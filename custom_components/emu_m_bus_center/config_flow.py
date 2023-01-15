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
    _sensor_tuples = {}
    _ip = ""

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            ip = user_input.get("ip", "")
            client = EmuApiClient(ip)
            valid_connection = await client.validate_connection_async(
                hass=self.hass, sensors=None
            )
            if valid_connection:
                sensor_ids = await client.scan_for_sensors_async(hass=self.hass)
                return await self.async_step_sensors(ip=ip, sensor_ids=sensor_ids)
            else:
                _LOGGER.error("async step_user determined invalid connection")
                # TODO: show abort dialog
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("ip"): TextSelector(
                        TextSelectorConfig(type=TextSelectorType.URL)
                    )
                }
            ),
        )

    async def async_step_sensors(self, user_input=None, ip=None, sensor_ids=None):
        if user_input is not None:
            sensors = list()
            for (_id, _serial) in self._sensor_tuples:
                sensors.append((_id, _serial, user_input.get(str(_id), "")))
            return self.async_create_entry(
                title="",
                data={
                    "ip": self._ip,
                    "sensors": sensors,
                },
            )

        else:
            schema = {}
            self._sensor_tuples = sensor_ids
            self._ip = ip
            for (_id, _serial) in sensor_ids:
                schema[vol.Required(f"{_id}")] = str
            return self.async_show_form(
                step_id="sensors", data_schema=vol.Schema(schema)
            )
