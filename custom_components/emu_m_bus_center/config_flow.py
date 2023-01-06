from __future__ import annotations

import logging

import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class CenterConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        if user_input is not None:
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
                    vol.Required("ip"): str,
                    vol.Required("sensors"): str,
                }  # TODO: properly validate the dict
            ),
        )
