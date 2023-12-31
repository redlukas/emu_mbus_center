from __future__ import annotations

import logging

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.selector import TextSelector
from homeassistant.helpers.selector import TextSelectorConfig
from homeassistant.helpers.selector import TextSelectorType
from homeassistant.util.network import is_ipv4_address
from homeassistant.util.network import is_ipv6_address

from . import EmuApiClient
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class CenterConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL
    _sensor_tuples = {}
    _ip = ""

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            ip = user_input.get("ip", "")
            if is_ipv4_address(ip) or is_ipv6_address(ip):
                client = EmuApiClient(ip)
                valid_connection = await client.validate_connection_async(
                    hass=self.hass, sensors=None
                )
                if valid_connection:
                    sensor_ids = await client.scan_for_sensors_async(hass=self.hass)
                    return self.async_create_entry(
                        title=user_input.get("name", "Emu M-Bus Center"),
                        data={
                            "sensors": sensor_ids,
                            "ip": ip,
                            "name": user_input.get("name", "Emu M-Bus Center"),
                        },
                    )
                else:
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
