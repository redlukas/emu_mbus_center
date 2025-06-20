"""Sensor implementation for a 24 Value Emu Professional sensor."""

import logging

from custom_components.emu_m_bus_center.const import (
    ACTIVE_ENERGY_EXPORT_TARIFF_1,
    ACTIVE_ENERGY_EXPORT_TARIFF_2,
    ACTIVE_ENERGY_IMPORT_TARIFF_1,
    ACTIVE_ENERGY_IMPORT_TARIFF_2,
    ACTIVE_POWER_ALL_PHASES,
    ACTIVE_POWER_PHASE_1,
    ACTIVE_POWER_PHASE_2,
    ACTIVE_POWER_PHASE_3,
    CURRENT_ALL_PHASES,
    CURRENT_PHASE_1,
    CURRENT_PHASE_2,
    CURRENT_PHASE_3,
    FORM_FACTOR_PHASE_1,
    FORM_FACTOR_PHASE_2,
    FORM_FACTOR_PHASE_3,
    FREQUENCY,
    POWER_FAILURES,
    REACTIVE_ENERGY_CAPACITIVE_TARIFF_1,
    REACTIVE_ENERGY_CAPACITIVE_TARIFF_2,
    REACTIVE_ENERGY_INDUCTIVE_TARIFF_1,
    REACTIVE_ENERGY_INDUCTIVE_TARIFF_2,
    VOLTAGE_PHASE_1,
    VOLTAGE_PHASE_2,
    VOLTAGE_PHASE_3,
)
from custom_components.emu_m_bus_center.sensor import (
    EmuActiveEnergySensor,
    EmuActivePowerSensor,
    EmuCoordinator,
    EmuCurrentSensor,
    EmuFormFactorSensor,
    EmuFrequencySensor,
    EmuPowerFailureSensor,
    EmuReactiveEnergySensor,
    EmuVoltageSensor,
)
from homeassistant.core import HomeAssistant


class EmuProfessionalV25_24val(EmuCoordinator):
    """Coordinator for a 24 Value Emu Professional sensor."""

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
        """Create a new Coordinator object for a 24 Value Emu Professional sensor."""
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
                "name": ACTIVE_ENERGY_IMPORT_TARIFF_1,
                "position": 0,
                "has_scaling_factor": True,
                "unit_str": "Wh",
                "description_str": "Energy",
                "sensor_class": EmuActiveEnergySensor,
            },
            {
                "name": ACTIVE_ENERGY_IMPORT_TARIFF_2,
                "position": 1,
                "has_scaling_factor": True,
                "unit_str": "Wh",
                "description_str": "Energy",
                "sensor_class": EmuActiveEnergySensor,
            },
            {
                "name": ACTIVE_ENERGY_EXPORT_TARIFF_1,
                "position": 2,
                "has_scaling_factor": True,
                "unit_str": "Wh",
                "description_str": "Energy",
                "sensor_class": EmuActiveEnergySensor,
            },
            {
                "name": ACTIVE_ENERGY_EXPORT_TARIFF_2,
                "position": 3,
                "has_scaling_factor": True,
                "unit_str": "Wh",
                "description_str": "Energy",
                "sensor_class": EmuActiveEnergySensor,
            },
            {
                "name": REACTIVE_ENERGY_INDUCTIVE_TARIFF_1,
                "position": 4,
                "has_scaling_factor": True,
                "unit_str": "Wh",
                "description_str": "Energy",
                "sensor_class": EmuReactiveEnergySensor,
            },
            {
                "name": REACTIVE_ENERGY_INDUCTIVE_TARIFF_2,
                "position": 5,
                "has_scaling_factor": True,
                "unit_str": "Wh",
                "description_str": "Energy",
                "sensor_class": EmuReactiveEnergySensor,
            },
            {
                "name": REACTIVE_ENERGY_CAPACITIVE_TARIFF_1,
                "position": 6,
                "has_scaling_factor": True,
                "unit_str": "Wh",
                "description_str": "Energy",
                "sensor_class": EmuReactiveEnergySensor,
            },
            {
                "name": REACTIVE_ENERGY_CAPACITIVE_TARIFF_2,
                "position": 7,
                "has_scaling_factor": True,
                "unit_str": "Wh",
                "description_str": "Energy",
                "sensor_class": EmuReactiveEnergySensor,
            },
            {
                "name": ACTIVE_POWER_ALL_PHASES,
                "position": 8,
                "has_scaling_factor": True,
                "unit_str": "W",
                "description_str": "Power",
                "sensor_class": EmuActivePowerSensor,
            },
            {
                "name": ACTIVE_POWER_PHASE_1,
                "position": 9,
                "has_scaling_factor": True,
                "unit_str": "W",
                "description_str": "Power (vendor specific)",
                "sensor_class": EmuActivePowerSensor,
            },
            {
                "name": ACTIVE_POWER_PHASE_2,
                "position": 10,
                "has_scaling_factor": True,
                "unit_str": "W",
                "description_str": "Power (vendor specific)",
                "sensor_class": EmuActivePowerSensor,
            },
            {
                "name": ACTIVE_POWER_PHASE_3,
                "position": 11,
                "has_scaling_factor": True,
                "unit_str": "W",
                "description_str": "Power (vendor specific)",
                "sensor_class": EmuActivePowerSensor,
            },
            {
                "name": CURRENT_ALL_PHASES,
                "position": 12,
                "has_scaling_factor": True,
                "unit_str": "A",
                "description_str": "Ampere",
                "sensor_class": EmuCurrentSensor,
            },
            {
                "name": CURRENT_PHASE_1,
                "position": 13,
                "has_scaling_factor": True,
                "unit_str": "A",
                "description_str": "Ampere (vendor specific)",
                "sensor_class": EmuCurrentSensor,
            },
            {
                "name": CURRENT_PHASE_2,
                "position": 14,
                "has_scaling_factor": True,
                "unit_str": "A",
                "description_str": "Ampere (vendor specific)",
                "sensor_class": EmuCurrentSensor,
            },
            {
                "name": CURRENT_PHASE_3,
                "position": 15,
                "has_scaling_factor": True,
                "unit_str": "A",
                "description_str": "Ampere (vendor specific)",
                "sensor_class": EmuCurrentSensor,
            },
            {
                "name": VOLTAGE_PHASE_1,
                "position": 16,
                "has_scaling_factor": True,
                "unit_str": "V",
                "description_str": "Volts (vendor specific)",
                "sensor_class": EmuVoltageSensor,
            },
            {
                "name": VOLTAGE_PHASE_2,
                "position": 17,
                "has_scaling_factor": True,
                "unit_str": "V",
                "description_str": "Volts (vendor specific)",
                "sensor_class": EmuVoltageSensor,
            },
            {
                "name": VOLTAGE_PHASE_3,
                "position": 18,
                "has_scaling_factor": True,
                "unit_str": "V",
                "description_str": "Volts (vendor specific)",
                "sensor_class": EmuVoltageSensor,
            },
            {
                "name": FORM_FACTOR_PHASE_1,
                "position": 19,
                "has_scaling_factor": False,
                "unit_str": "None",
                "description_str": "Special supplier information",
                "sensor_class": EmuFormFactorSensor,
            },
            {
                "name": FORM_FACTOR_PHASE_2,
                "position": 20,
                "has_scaling_factor": False,
                "unit_str": "None",
                "description_str": "Special supplier information",
                "sensor_class": EmuFormFactorSensor,
            },
            {
                "name": FORM_FACTOR_PHASE_3,
                "position": 21,
                "has_scaling_factor": False,
                "unit_str": "None",
                "description_str": "Special supplier information",
                "sensor_class": EmuFormFactorSensor,
            },
            {
                "name": FREQUENCY,
                "position": 22,
                "has_scaling_factor": False,
                "unit_str": "None",
                "description_str": "Special supplier information",
                "sensor_class": EmuFrequencySensor,
            },
            {
                "name": POWER_FAILURES,
                "position": 23,
                "has_scaling_factor": True,
                "unit_str": "None",
                "description_str": "Reset counter",
                "sensor_class": EmuPowerFailureSensor,
            },
        ]

    @property
    def version_number(self) -> int:
        """Get the Version number of this device."""
        return 25

    @property
    def sensor_count(self) -> int:
        """Get the sensor count."""
        return 24

    @property
    def model_name(self) -> str:
        """Get the model name."""
        return "Professional II 3/100"

    @property
    def manufacturer_name(self) -> str:
        """Get the manufacturer name."""
        return "EMU"
