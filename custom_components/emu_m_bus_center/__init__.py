"""The Emu M-Bus Center integration."""

from __future__ import annotations

import json
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import issue_registry as ir

from .const import DOMAIN
from .device_types.devices import generic_sensor_deserializer
from .emu_client import EmuApiClient

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up Emu M-Bus Center from a config entry."""

    hass.data.setdefault(DOMAIN, {})

    client = EmuApiClient(ip=config_entry.data["ip"])
    # _LOGGER.error("setup_entry in __init__. data is: %s", config_entry.data)  # removeme

    # Detecting unserialized sensors
    unserialized_sensors = config_entry.data.get("sensors")
    if unserialized_sensors:
        ir.async_create_issue(
            hass,
            domain=DOMAIN,
            issue_id="migration_to_serialized_sensors",
            is_fixable=False,
            severity=ir.IssueSeverity.ERROR,
            translation_key="migration_to_serialized_sensors",
            learn_more_url="https://github.com/redlukas/emu_mbus_center/releases/tag/v2.0.0",
        )

    # Loading from serialized sensors
    serialized_sensors = config_entry.data["serialized_sensors"]
    # _LOGGER.error(
    #     "Fresh from the serialized_sensors: %s, loaded_unserialized_config is %s",
    #     serialized_sensors,
    #     loaded_unserialized_config,
    # )  # removeme
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
