"""Sensor implementation for a 15 Value Emu sensor."""

import logging

from custom_components.emu_m_bus_center.const import (
    ACTIVE_ENERGY_IMPORT,
    ACTIVE_ENERGY_IMPORT_RESETTABLE,
    ACTIVE_POWER,
    CURRENT,
    ERROR_FLAGS,
    FORM_FACTOR,
    FREQUENCY,
    SERIAL_NO,
    VOLTAGE,
)
from custom_components.emu_m_bus_center.sensor import (
    EmuActiveEnergyResettableSensor,
    EmuActiveEnergySensor,
    EmuActivePowerSensor,
    EmuCoordinator,
    EmuCurrentSensor,
    EmuErrorSensor,
    EmuFormFactorSensor,
    EmuFrequencySensor,
    EmuSerialNoSensor,
    EmuVoltageSensor,
)
from homeassistant.core import HomeAssistant


class Emu_1_40_V4_15val(EmuCoordinator):
    """Coordinator for a 15 Value Emu sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry_id: str,
        logger: logging.Logger,
        sensor_id: int,
        serial_no: str,
        center_name: str,
        sensor_given_name: str,
    ) -> None:
        """Create a new Coordinator object for a 15 Value Emu sensor."""
        self._config_entry_id = config_entry_id
        self._hass = hass
        self._name = (
            sensor_given_name if sensor_given_name else f"{sensor_id}/{serial_no}"
        )
        self._sensor_id = sensor_id
        self._logger = logger
        self._serial_no = serial_no
        self._center_name = center_name
        self._config = dict(
            self._hass.config_entries.async_get_entry(self._config_entry_id).data
        )

        super().__init__(
            hass=hass,
            config_entry_id=config_entry_id,
            logger=logger,
            sensor_id=sensor_id,
            serial_no=serial_no,
            center_name=center_name,
            sensor_given_name=sensor_given_name,
        )
        self._sensors = [
            {
                "name": VOLTAGE,
                "position": 0,
                "has_scaling_factor": True,
                "unit_str": "V",
                "description_str": "Volts (vendor specific)",
                "sensor_class": EmuVoltageSensor,
            },
            {
                "name": CURRENT,
                "position": 1,
                "has_scaling_factor": True,
                "unit_str": "A",
                "description_str": "Ampere (vendor specific)",
                "sensor_class": EmuCurrentSensor,
            },
            {
                "name": FORM_FACTOR,
                "position": 2,
                "has_scaling_factor": True,
                "unit_str": "None",
                "description_str": "Special supplier information",
                "sensor_class": EmuFormFactorSensor,
            },
            {
                "name": ACTIVE_POWER,
                "position": 3,
                "has_scaling_factor": True,
                "unit_str": "W",
                "description_str": "Power",
                "sensor_class": EmuActivePowerSensor,
            },
            {
                "name": FREQUENCY,
                "position": 4,
                "has_scaling_factor": True,
                "unit_str": "Hz",
                "description_str": "Frequency",
                "sensor_class": EmuFrequencySensor,
            },
            {
                "name": ACTIVE_ENERGY_IMPORT,
                "position": 5,
                "has_scaling_factor": True,
                "unit_str": "Wh",
                "description_str": "Energy",
                "sensor_class": EmuActiveEnergySensor,
            },
            {
                "name": ACTIVE_ENERGY_IMPORT_RESETTABLE,
                "position": 6,
                "has_scaling_factor": True,
                "unit_str": "Wh",
                "description_str": "Energy",
                "sensor_class": EmuActiveEnergyResettableSensor,
            },
            {
                "name": SERIAL_NO,
                "position": 7,
                "has_scaling_factor": False,
                "unit_str": "None",
                "description_str": None,
                "sensor_class": EmuSerialNoSensor,
            },
            {
                "name": ERROR_FLAGS,
                "position": 12,
                "has_scaling_factor": False,
                "unit_str": "Bin",
                "description_str": "Error flags (Device type specific)",
                "sensor_class": EmuErrorSensor,
            },
        ]

    @property
    def version_number(self) -> int:
        """Get the Version number of this device."""
        return 4

    @property
    def sensor_count(self) -> int:
        """Get the sensor count."""
        return 15

    @property
    def model_name(self) -> str:
        """Get the model name."""
        return "1/40"

    @property
    def manufacturer_name(self) -> str:
        """Get the manufacturer name."""
        return "EMU"
