"""Config flow for Emu M-Bus Center."""

from __future__ import annotations

import json
import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers.selector import (
    TextSelector,
    TextSelectorConfig,
    TextSelectorType,
)
from homeassistant.util.network import is_ipv4_address, is_ipv6_address

from . import EmuApiClient
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class CenterConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Implement the config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL
    _sensor_tuples = {}
    _ip = ""

    async def async_step_user(self, user_input=None):
        """Get the config details from the user."""
        errors = {}
        if user_input is not None:
            ip = user_input.get("ip", "")
            if is_ipv4_address(ip) or is_ipv6_address(ip):
                client = EmuApiClient(ip=ip)
                connection_info = await client.validate_connection_async(sensors=None)
                _LOGGER.debug("async_step_user got connectionInfo %s", connection_info)
                if connection_info and connection_info.get("found_center"):
                    sensors = await client.scan_for_sensors_async()
                    sensor_dicts = [sensor.to_dict() for sensor in sensors]
                    return self.async_create_entry(
                        title=user_input.get("name", "Emu M-Bus Center"),
                        data={
                            "sensors": json.dumps(sensor_dicts),
                            "ip": ip,
                            "name": user_input.get("name", "Emu M-Bus Center"),
                        },
                    )
                _LOGGER.error("async step_user determined invalid connection")
                errors["base"] = "invalid_connection"
            else:
                _LOGGER.error("user input is invalid IP")
                errors["invalid_ip"] = "invalid_ip"
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("ip"): TextSelector(
                        TextSelectorConfig(type=TextSelectorType.URL)
                    ),
                    vol.Required("name"): str,
                }
            ),
            errors=errors,
        )
