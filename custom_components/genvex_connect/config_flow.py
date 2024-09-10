"""Config flow for Genvex Connect integration."""

from __future__ import annotations

import logging
from typing import Any, Dict, Mapping

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.exceptions import HomeAssistantError
from genvexnabto import GenvexNabto, GenvexNabtoConnectionErrorType # type: ignore

from .const import DOMAIN, CONF_DEVICE_ID, CONF_AUTHORIZED_EMAIL, CONF_DEVICE_IP, CONF_DEVICE_PORT

_LOGGER = logging.getLogger(__name__)


class GenvexConnectConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle the config flow for Genvex Connect."""

    VERSION = 1
    
    _authorized_email:str = ""
    _device_id:str|None = None
    _device_ip:str|None = None
    _device_port:int = 5570

    def __init__(self) -> None:
        """Initialize."""
        _LOGGER.info("Starting config flow")
        self._genvex_nabto = GenvexNabto()
        self._genvex_nabto.open_socket()
        self._genvex_nabto.start_listening()

    async def async_step_user(self, user_input: Dict[str, Any] | None = None) -> ConfigFlowResult:
        """Handle the initial step."""
        devices = await self._genvex_nabto.discover_devices(True)
        _LOGGER.info(devices)
        return self.async_show_select_form()

    def async_show_select_form(self):
        """Show the select device form."""
        _LOGGER.info("Found %s on the network", self._genvex_nabto.get_discovered_devices())

        deviceList = list(self._genvex_nabto.get_discovered_devices().keys())
        deviceList += ["Manual"]
        _LOGGER.info(deviceList)

        data_schema = {
            vol.Required(
                CONF_DEVICE_ID,
            ): vol.In(deviceList),
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
            self._genvex_nabto.get_discovered_devices(),
        )
        selected_device = self._genvex_nabto.get_discovered_devices()[selected_device_id]
        self._device_ip = selected_device[0]
        self._device_port = selected_device[1]
        self._genvex_nabto.set_device(selected_device_id)
        _LOGGER.info(
            "Selected %s with IP: %s and port: %s",
            selected_device_id,
            self._device_ip,
            self._device_port,
        )

        return self.async_show_device_form()

    def async_show_device_form(self, invalid_email:bool=False, connection_timeout:bool=False):
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

        return self.async_show_form(step_id="device", data_schema=vol.Schema(data_schema), errors=errors)

    async def async_step_device(self, user_input:Dict[str, str]) -> ConfigFlowResult:
        """After user has provided their email. Try to connect and see if email is correct."""
        _LOGGER.info("Async step device - user has picked {%s}", user_input)

        self._device_id = user_input[CONF_DEVICE_ID]
        self._authorized_email = user_input[CONF_AUTHORIZED_EMAIL]
        
        _LOGGER.info("User provided email: %s", self._authorized_email)
        self._genvex_nabto.set_email(self._authorized_email)
        self._genvex_nabto.connect_to_device()
        await self._genvex_nabto.wait_for_connection()
        if self._genvex_nabto.get_connection_error() is not None:
            if self._genvex_nabto.get_connection_error() is GenvexNabtoConnectionErrorType.AUTHENTICATION_ERROR:
                if self._authorized_email.lower() == self._authorized_email:
                    return self.async_show_device_form(invalid_email=True)
                user_input[CONF_AUTHORIZED_EMAIL] = self._authorized_email.lower()
                return await self.async_step_device(user_input)
            if self._genvex_nabto.get_connection_error() is GenvexNabtoConnectionErrorType.TIMEOUT:
                return self.async_show_device_form(connection_timeout=True)
            if self._genvex_nabto.get_connection_error() is GenvexNabtoConnectionErrorType.UNSUPPORTED_MODEL:
                _LOGGER.warning(
                    f"Tried to connect to device with unsupported model. Model no: {self._genvex_nabto.get_device_model()}, device number: {self._genvex_nabto.get_device_number()}, slavedevice number: {self._genvex_nabto.get_slave_device_number()}, and slavedevice model: {self._genvex_nabto.get_slave_device_model()}"
                )
                return self.async_abort(reason="unsupported_model")
        _LOGGER.info("Is connected to Genvex device successfully.")
        config_data = {
            CONF_DEVICE_ID: self._device_id,
            CONF_AUTHORIZED_EMAIL: self._authorized_email,
        }
        return self.async_create_entry(title=self._device_id, data=config_data)

    def async_show_manual_form(self, invalid_email:bool=False, connection_timeout:bool=False):
        """Show the manual form."""
        data_schema:Dict[vol.Required, type] = {
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

        return self.async_show_form(step_id="manual", data_schema=vol.Schema(data_schema), errors=errors)

    async def async_step_manual(self, user_input:Dict[str, str]) -> ConfigFlowResult:
        """After user has provided their ip, port and email. Try to connect and see if email is correct."""
        _LOGGER.info("Async step manual - user has picked {%s}", user_input)

        self._device_id = user_input[CONF_DEVICE_ID]
        self._authorized_email = user_input[CONF_AUTHORIZED_EMAIL]
        self._device_ip = user_input[CONF_DEVICE_IP]
        self._device_port = int(user_input[CONF_DEVICE_PORT])

        _LOGGER.info("User provided email: %s, ip: %s, port: %s", self._authorized_email, self._device_ip, self._device_port)

        self._genvex_nabto.set_email(self._authorized_email)
        self._genvex_nabto.set_device(self._device_id, self._device_ip, self._device_port)
        self._genvex_nabto.connect_to_device()
        await self._genvex_nabto.wait_for_connection()
        if self._genvex_nabto.get_connection_error() is not None:
            if self._genvex_nabto.get_connection_error() is GenvexNabtoConnectionErrorType.AUTHENTICATION_ERROR:
                if self._authorized_email.lower() == self._authorized_email:
                    return self.async_show_manual_form(invalid_email=True)
                user_input[CONF_AUTHORIZED_EMAIL] = self._authorized_email.lower()
                return await self.async_step_manual(user_input)
            if self._genvex_nabto.get_connection_error() is GenvexNabtoConnectionErrorType.TIMEOUT:
                return self.async_show_manual_form(connection_timeout=True)
            if self._genvex_nabto.get_connection_error() is GenvexNabtoConnectionErrorType.UNSUPPORTED_MODEL:
                _LOGGER.warning(
                    f"Tried to connect to device with unsupported model. Model no: {self._genvex_nabto.get_device_model()}, device number: {self._genvex_nabto.get_device_number()}, slavedevice number: {self._genvex_nabto.get_slave_device_number()}, and slavedevice model: {self._genvex_nabto.get_slave_device_model()}"
                )
                return self.async_abort(reason="unsupported_model")
            
        _LOGGER.info("Is connected to Genvex device successfully.")
        config_data:Mapping[str, Any] = {
            CONF_DEVICE_ID: self._device_id,
            CONF_DEVICE_IP: self._device_ip,
            CONF_DEVICE_PORT: self._device_port,
            CONF_AUTHORIZED_EMAIL: self._authorized_email,
        }
        return self.async_create_entry(title=self._device_id, data=config_data)


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
