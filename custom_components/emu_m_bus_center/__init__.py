"""The Emu M-Bus Center integration."""

from __future__ import annotations

import json
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .device_types.devices import generic_sensor_deserializer
from .emu_client import EmuApiClient

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up Emu M-Bus Center from a config entry."""

    hass.data.setdefault(DOMAIN, {})

    client = EmuApiClient(ip=config_entry.data["ip"])
    serialized_sensors = config_entry.data["sensors"]
    sensors_from_config = json.loads(
        serialized_sensors, object_hook=generic_sensor_deserializer
    )

    connection_info = await client.validate_connection_async(
        sensors=sensors_from_config
    )

    _LOGGER.debug("async_setup_entry got connectionInfo %s", connection_info)

    if not connection_info:
        _LOGGER.error("__init__ did not get the correct return dict")
        return False

    if not connection_info.get("found_center"):
        _LOGGER.error("__init__ did not find a center")

    if not connection_info.get("found_all_sensors"):
        _LOGGER.error("__init__ did not find all sensors")

    hass.data[DOMAIN][config_entry.entry_id] = client

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
