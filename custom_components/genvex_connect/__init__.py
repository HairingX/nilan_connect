"""The Genvex Connect integration."""

from __future__ import annotations
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady, ConfigEntryAuthFailed

from genvexnabto import GenvexNabto, GenvexNabtoConnectionErrorType # type: ignore

from custom_components.genvex_connect.data import GenvexConnectHassData, get_hass_data, remove_hass_data, set_hass_data # type: ignore
from .const import DOMAIN, CONF_DEVICE_ID, CONF_AUTHORIZED_EMAIL, CONF_DEVICE_IP, CONF_DEVICE_PORT

_LOGGER = logging.getLogger(__name__)
PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.CLIMATE,
    Platform.SWITCH,
    Platform.NUMBER,
    Platform.BUTTON,
    Platform.SELECT,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Genvex Connect from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    authorized_email = str(entry.data.get(CONF_AUTHORIZED_EMAIL))
    genvexnabto = GenvexNabto(authorized_email)
    device_id = str(entry.data.get(CONF_DEVICE_ID))
    device_ip = str(entry.data.get(CONF_DEVICE_IP))
    device_port = int(entry.data.get(CONF_DEVICE_PORT, 0))
    genvexnabto.set_device(device_id, device_ip, device_port)

    discoveryResult = await genvexnabto.wait_for_discovery()
    if discoveryResult is False:  # Waits for GenvexNabto to discover the current device IP
        raise ConfigEntryNotReady(f"Timed out while trying to discover {device_id}")
    genvexnabto.connect_to_device()
    await genvexnabto.wait_for_connection()
    _LOGGER.info(f"Controller model: {genvexnabto.get_device_model()}")
    if genvexnabto.get_connection_error() is not False:
        if genvexnabto.get_connection_error() is GenvexNabtoConnectionErrorType.AUTHENTICATION_ERROR:
            raise ConfigEntryAuthFailed(f"Credentials expired for {device_id}")
        if genvexnabto.get_connection_error() is GenvexNabtoConnectionErrorType.TIMEOUT:
            raise ConfigEntryNotReady(f"Timed out while trying to connect to {device_id}")
        if genvexnabto.get_connection_error() is GenvexNabtoConnectionErrorType.UNSUPPORTED_MODEL:
            raise ConfigEntryNotReady(
                f"Timed out while trying to get data from {device_id} did not correctly load a model for Model no: {genvexnabto.get_device_model()}, device number: {genvexnabto.get_device_number()} and slavedevice number: {genvexnabto.get_slave_device_number()}"
            )

    dataResult = await genvexnabto.wait_for_data()
    if dataResult is False:  # Waits for GenvexNabto to get fresh data
        if genvexnabto.get_loaded_model_name() is None:
            raise ConfigEntryNotReady(
                f"Timed out while trying to get data from {device_id} did not correctly load a model for Model no: {genvexnabto.get_device_model()}, device number: {genvexnabto.get_device_number()} and slavedevice number: {genvexnabto.get_slave_device_number()}"
            )
        _LOGGER.error(f"Could not get data from {device_id} has loaded model for {genvexnabto.get_loaded_model_name()}")
        raise ConfigEntryNotReady(
            f"Timed out while trying to get data from {device_id} has loaded model for {genvexnabto.get_loaded_model_name()}"
        )

    data = GenvexConnectHassData(genvexnabto=genvexnabto)
    set_hass_data(hass, entry, data)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    genvexnabto.notify_all_update_handlers()
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    data = get_hass_data(hass, entry)
    data["genvexnabto"].stop_listening()
    remove_hass_data(hass, entry)    
    return True


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)