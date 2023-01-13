from __future__ import annotations

import logging

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.selector import TextSelector
from homeassistant.helpers.selector import TextSelectorConfig
from homeassistant.helpers.selector import TextSelectorType

from . import EmuApiClient
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class CenterConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            ip = user_input.get("ip", "")
            client = EmuApiClient(ip)
            valid_connection = await client.validate_connection_async(
                hass=self.hass, sensors=None
            )
            if valid_connection:
                _LOGGER.error("async step_user determined valid connection")
                sensor_ids = await client.scan_for_sensors_async(hass=self.hass)
                _LOGGER.debug(f"found sensors {sensor_ids}")
                return self.async_create_entry(
                    title="",
                    data={
                        "ip": user_input.get("ip", ""),
                        "sensors": user_input.get("sensors", ""),
                    },
                )
            else:
                _LOGGER.error("async step_user determined invalid connection")
                return self.async_create_entry(
                    title="",
                    data={
                        "ip": user_input.get("ip", ""),
                        "sensors": user_input.get("sensors", ""),
                    },
                )
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("ip"): TextSelector(
                        TextSelectorConfig(type=TextSelectorType.URL)
                    ),
                    vol.Required("sensors"): str,
                }  # TODO: properly validate the dict
            ),
        )
