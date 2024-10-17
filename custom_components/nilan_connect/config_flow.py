"""Config flow for Nilan Connect integration."""

from __future__ import annotations

import logging
from typing import Any, Dict, Mapping

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.exceptions import HomeAssistantError
from nilan_proxy import NilanProxy, NilanProxyConnectionErrorType # type: ignore

from .const import DOMAIN, CONF_DEVICE_ID, CONF_AUTHORIZED_EMAIL, CONF_DEVICE_IP, CONF_DEVICE_PORT

_LOGGER = logging.getLogger(__name__)


class NilanConnectConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle the config flow for Nilan Connect."""

    VERSION = 1

    _authorized_email:str = ""
    _device_id:str = ""
    _device_ip:str = ""
    _device_port:int = 5570

    def __init__(self) -> None:
        """Initialize."""
        _LOGGER.info("Starting config flow")
        self._proxy = NilanProxy()
        self._proxy.open_socket()
        self._proxy.start_listening()

    async def async_step_user(self, user_input: Dict[str, Any] | None = None) -> ConfigFlowResult:
        """Invoked when a user initiates a flow via the user interface."""
        devices = await self._proxy.discover_devices(True)
        _LOGGER.info(devices)
        return self.async_show_select_form()

    def async_show_select_form(self) -> ConfigFlowResult:
        """Show the select device form."""
        _LOGGER.info("Found %s on the network", self._proxy.get_discovered_devices())

        deviceList = list(self._proxy.get_discovered_devices().keys())
        deviceList += ["Manual"]
        _LOGGER.info(deviceList)

        data_schema = {
            vol.Required(CONF_DEVICE_ID): vol.In(deviceList),
        }

        return self.async_show_form(step_id="pick", data_schema=vol.Schema(data_schema), errors={})

    async def async_step_pick(self, user_input:Dict[str, str]) -> ConfigFlowResult:
        """After user has picked a device"""
        _LOGGER.info("Async step user has picked {%s}", user_input)

        self._device_id = "Nilan"

        selected_device_id = user_input[CONF_DEVICE_ID]
        if selected_device_id == "Manual":
            return self.async_show_manual_form()

        _LOGGER.info(
            "Previously, the user selected device %s to configure, locate it in %s",
            selected_device_id,
            self._proxy.get_discovered_devices(),
        )
        selected_device = self._proxy.get_discovered_devices()[selected_device_id]
        self._device_ip = selected_device[0]
        self._device_port = selected_device[1]
        self._proxy.set_device(selected_device_id)
        _LOGGER.info(
            "Selected %s with IP: %s and port: %s",
            selected_device_id,
            self._device_ip,
            self._device_port,
        )

        return self.async_show_device_form()

    def async_show_device_form(self, invalid_email:bool=False, connection_timeout:bool=False, deviceid_already_in_use:bool=False) -> ConfigFlowResult:
        """Show the device form."""
        data_schema = {
            vol.Required(CONF_DEVICE_ID, default=self._device_id): str,
            vol.Required(CONF_AUTHORIZED_EMAIL): str,
        }

        errors:Dict[str,str] = {}
        if invalid_email:
            errors["base"] = "invalid_auth"
        if connection_timeout:
            errors["base"] = "cannot_connect"
        if deviceid_already_in_use:
            errors["base"] = "deviceid_already_in_use"

        return self.async_show_form(step_id="device", data_schema=vol.Schema(data_schema), errors=errors)

    async def async_step_device(self, user_input:Dict[str, str]) -> ConfigFlowResult:
        """After user has provided their email. Try to connect and see if email is correct."""
        _LOGGER.info("Async step device - user has picked {%s}", user_input)

        self._device_id = user_input[CONF_DEVICE_ID]
        self._authorized_email = user_input[CONF_AUTHORIZED_EMAIL]

        _LOGGER.info("User provided email: %s", self._authorized_email)
        self._proxy.set_email(self._authorized_email)
        self._proxy.connect_to_device()
        await self._proxy.wait_for_connection()
        if self._proxy.get_connection_error() is not None:
            if self._proxy.get_connection_error() is NilanProxyConnectionErrorType.AUTHENTICATION_ERROR:
                if self._authorized_email.lower() == self._authorized_email:
                    return self.async_show_device_form(invalid_email=True)
                user_input[CONF_AUTHORIZED_EMAIL] = self._authorized_email.lower()
                return await self.async_step_device(user_input)
            if self._proxy.get_connection_error() is NilanProxyConnectionErrorType.TIMEOUT:
                return self.async_show_device_form(connection_timeout=True)
            if self._proxy.get_connection_error() is NilanProxyConnectionErrorType.UNSUPPORTED_MODEL:
                _LOGGER.warning(
                    f"Tried to connect to device with unsupported model. Model no: {self._proxy.get_device_model()}, device number: {self._proxy.get_device_number()}, slavedevice number: {self._proxy.get_slave_device_number()}, and slavedevice model: {self._proxy.get_slave_device_model()}"
                )
                return self.async_abort(reason="unsupported_model")
        _LOGGER.info("Is connected to device successfully.")
        config_data = {
            CONF_DEVICE_ID: self._device_id,
            CONF_AUTHORIZED_EMAIL: self._authorized_email,
        }
        return self.async_create_entry(title=self._device_id, data=config_data)

    def async_show_manual_form(self, invalid_email:bool=False, connection_timeout:bool=False, deviceid_already_in_use:bool=False) -> ConfigFlowResult:
        """Show the manual form."""
        data_schema:Dict[vol.Required|vol.Optional, type] = {
            vol.Required(CONF_DEVICE_ID, default=self._device_id): str,
            vol.Required(CONF_DEVICE_IP, default=self._device_ip): str,
            vol.Required(CONF_DEVICE_PORT, default=self._device_port): int,
            vol.Required(CONF_AUTHORIZED_EMAIL, default=self._authorized_email): str,
        }

        errors:Dict[str,str] = {}
        if invalid_email:
            errors["base"] = "invalid_auth"
        if connection_timeout:
            errors["base"] = "cannot_connect"
        if deviceid_already_in_use:
            errors["base"] = "deviceid_already_in_use"

        return self.async_show_form(step_id="manual", data_schema=vol.Schema(data_schema), errors=errors)

    async def async_step_manual(self, user_input:Dict[str, Any]) -> ConfigFlowResult:
        """After user has provided their ip, port and email. Try to connect and see if email is correct."""
        _LOGGER.info("Async step manual - user has picked {%s}", user_input)

        device_id = user_input.get(CONF_DEVICE_ID, self._device_id) or ""
        config_entry = await self.async_set_unique_id(device_id)
        if config_entry: return self.async_show_manual_form(deviceid_already_in_use=True)

        connection_error = await self._async_connect_with_settings(user_input)

        if len(self._device_id.strip()) == 0: return self.async_abort(reason="Device ID must be set")
        if len(self._device_ip.strip()) == 0: return self.async_abort(reason="Device IP must be set")

        if connection_error is not None:
            if connection_error is NilanProxyConnectionErrorType.AUTHENTICATION_ERROR:
                if self._authorized_email.lower() == self._authorized_email:
                    return self.async_show_manual_form(invalid_email=True)
                user_input[CONF_AUTHORIZED_EMAIL] = self._authorized_email.lower()
                return await self.async_step_manual(user_input)
            if connection_error is NilanProxyConnectionErrorType.TIMEOUT:
                return self.async_show_manual_form(connection_timeout=True)
            if connection_error is NilanProxyConnectionErrorType.UNSUPPORTED_MODEL:
                _LOGGER.warning(f"Tried to connect to device with unsupported model. Model no: {self._proxy.get_device_model()}, device number: {self._proxy.get_device_number()}, slavedevice number: {self._proxy.get_slave_device_number()}, and slavedevice model: {self._proxy.get_slave_device_model()}")
                return self.async_abort(reason="unsupported_model")

        config_data:Mapping[str, Any] = {
            CONF_DEVICE_ID: self._device_id,
            CONF_AUTHORIZED_EMAIL: self._authorized_email,
            CONF_DEVICE_IP: self._device_ip,
            CONF_DEVICE_PORT: self._device_port,
        }
        return self.async_create_entry(title=self._device_id, data=config_data)

    async def _async_connect_with_settings(self, user_input:Dict[str, Any]) -> NilanProxyConnectionErrorType|None:

        self._device_id = user_input.get(CONF_DEVICE_ID, self._device_id) or ""
        self._authorized_email = user_input.get(CONF_AUTHORIZED_EMAIL, self._authorized_email)
        self._device_ip = user_input.get(CONF_DEVICE_IP, self._device_ip)
        self._device_port = int(user_input.get(CONF_DEVICE_PORT, self._device_port))

        self._authorized_email = self._authorized_email.strip()
        self._device_id = self._device_id.strip()
        self._device_ip = self._device_ip.strip()

        _LOGGER.info("User provided id: %s, email: %s, ip: %s, port: %s", self._device_id, self._authorized_email, self._device_ip, self._device_port)

        self._proxy.set_email(self._authorized_email)
        if self._device_ip != "":
            self._proxy.set_device(self._device_id, self._device_ip, self._device_port)
        self._proxy.connect_to_device()
        await self._proxy.wait_for_connection()
        if self._proxy.get_connection_error() is not None:
            _LOGGER.info("Failed to connected to device.")
            return self._proxy.get_connection_error()

        _LOGGER.info("Is connected to device successfully.")
        return None

    async def async_step_reconfigure(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Handle the reconfigure step."""
        config_entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
        if config_entry is None: return self.async_abort(reason="missing entry data")
        data = config_entry.data

        if user_input is not None:
            # user has input his values
            connection_error = await self._async_connect_with_settings(user_input)
            if connection_error is not None:
                if connection_error is NilanProxyConnectionErrorType.AUTHENTICATION_ERROR:
                    if self._authorized_email.lower() == self._authorized_email:
                        return self.async_show_reconfigure_form(invalid_email=True)
                    user_input[CONF_AUTHORIZED_EMAIL] = self._authorized_email.lower()
                    return self.async_show_reconfigure_form()
                if connection_error is NilanProxyConnectionErrorType.TIMEOUT:
                    return self.async_show_manual_form(connection_timeout=True)
                if connection_error is NilanProxyConnectionErrorType.UNSUPPORTED_MODEL:
                    _LOGGER.warning(f"Tried to connect to device with unsupported model. Model no: {self._proxy.get_device_model()}, device number: {self._proxy.get_device_number()}, slavedevice number: {self._proxy.get_slave_device_number()}, and slavedevice model: {self._proxy.get_slave_device_model()}")
                    return self.async_abort(reason="unsupported_model")
            else:
                config_data:Mapping[str, Any] = {
                    CONF_DEVICE_ID: self._device_id,
                    CONF_AUTHORIZED_EMAIL: self._authorized_email,
                    CONF_DEVICE_IP: self._device_ip,
                    CONF_DEVICE_PORT: self._device_port,
                    }
                return self.async_update_reload_and_abort(
                        config_entry,
                        unique_id=config_entry.unique_id,
                        data=config_data,
                        reason="reconfigure_successful",
                    )

        # user has just initiated reconfigure

        self._device_id = data.get(CONF_DEVICE_ID, "").strip()
        self._authorized_email = data.get(CONF_AUTHORIZED_EMAIL, "").strip()
        self._device_ip = data.get(CONF_DEVICE_IP, "").strip()
        self._device_port = int(data.get(CONF_DEVICE_PORT, self._device_port))

        return self.async_show_reconfigure_form()

    def async_show_reconfigure_form(self, invalid_email:bool=False, connection_timeout:bool=False) -> ConfigFlowResult:
        """Show the reconfig form."""
        # process user input
        if self._device_ip == "": #device picked
            data_schema:Dict[vol.Required|vol.Optional, type] = {
                vol.Required(CONF_AUTHORIZED_EMAIL, default=self._authorized_email): str,
                vol.Optional(CONF_DEVICE_IP, default=self._device_ip): str,
                vol.Required(CONF_DEVICE_PORT, default=self._device_port): int,
            }
        else:
            data_schema:Dict[vol.Required|vol.Optional, type] = {
                vol.Required(CONF_AUTHORIZED_EMAIL, default=self._authorized_email): str,
                vol.Required(CONF_DEVICE_IP, default=self._device_ip): str,
                vol.Required(CONF_DEVICE_PORT, default=self._device_port): int,
            }

        errors:Dict[str,str] = {}
        if invalid_email:
            errors["base"] = "invalid_auth"
        if connection_timeout:
            errors["base"] = "cannot_connect"

        return self.async_show_form(step_id="reconfigure", data_schema=vol.Schema(data_schema), errors=errors)


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
