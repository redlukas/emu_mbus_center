"""The Emu M-Bus Center integration."""
from __future__ import annotations

import json
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .emu_client import EmuApiClient

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up Emu M-Bus Center from a config entry."""
    _LOGGER.warning("Running __init__.async_setup_entry")

    hass.data.setdefault(DOMAIN, {})

    client = EmuApiClient(config_entry.data["ip"])
    parsed = json.loads(config_entry.data["sensors"])

    valid_connection = await client.validate_connection_async(hass=hass, sensors=parsed)

    if not valid_connection:
        return False

    hass.data[DOMAIN][config_entry.entry_id] = client

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
