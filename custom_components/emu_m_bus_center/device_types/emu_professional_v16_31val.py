"""Sensor implementation for a 31 Value Emu Professional sensor."""

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
    APPARENT_POWER_ALL_PHASES,
    CURRENT_ALL_PHASES,
    CURRENT_PHASE_1,
    CURRENT_PHASE_2,
    CURRENT_PHASE_3,
    CURRENT_TRANSFORMER_FACTOR,
    ERROR_FLAGS,
    FORM_FACTOR_PHASE_1,
    FORM_FACTOR_PHASE_2,
    FORM_FACTOR_PHASE_3,
    FREQUENCY,
    POWER_FAILURES,
    REACTIVE_ENERGY_CAPACITIVE_TARIFF_1,
    REACTIVE_ENERGY_CAPACITIVE_TARIFF_2,
    REACTIVE_ENERGY_INDUCTIVE_TARIFF_1,
    REACTIVE_ENERGY_INDUCTIVE_TARIFF_2,
    REACTIVE_POWER_ALL_PHASES,
    REACTIVE_POWER_PHASE_1,
    REACTIVE_POWER_PHASE_2,
    REACTIVE_POWER_PHASE_3,
    VOLTAGE_PHASE_1,
    VOLTAGE_PHASE_2,
    VOLTAGE_PHASE_3,
)
from custom_components.emu_m_bus_center.sensor import (
    EmuActiveEnergySensor,
    EmuActivePowerSensor,
    EmuApparentPowerSensor,
    EmuCoordinator,
    EmuCurrentSensor,
    EmuErrorSensor,
    EmuFormFactorSensor,
    EmuFrequencySensor,
    EmuPowerFailureSensor,
    EmuReactiveEnergySensor,
    EmuReactivePowerSensor,
    EmuTransformerFactorSensor,
    EmuVoltageSensor,
)
from homeassistant.core import HomeAssistant


class EmuProfessionalV16_31val(EmuCoordinator):
    """Coordinator for a 32 Value Emu Professional sensor."""

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
        """Create a new Coordinator object for a 31 Value Emu Professional sensor."""
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
                "name": ACTIVE_POWER_PHASE_1,
                "position": 8,
                "has_scaling_factor": True,
                "unit_str": "W",
                "description_str": "Power (vendor specific)",
                "sensor_class": EmuActivePowerSensor,
            },
            {
                "name": ACTIVE_POWER_PHASE_2,
                "position": 9,
                "has_scaling_factor": True,
                "unit_str": "W",
                "description_str": "Power (vendor specific)",
                "sensor_class": EmuActivePowerSensor,
            },
            {
                "name": ACTIVE_POWER_PHASE_3,
                "position": 10,
                "has_scaling_factor": True,
                "unit_str": "W",
                "description_str": "Power (vendor specific)",
                "sensor_class": EmuActivePowerSensor,
            },
            {
                "name": ACTIVE_POWER_ALL_PHASES,
                "position": 11,
                "has_scaling_factor": True,
                "unit_str": "W",
                "description_str": "Power",
                "sensor_class": EmuActivePowerSensor,
            },
            {
                "name": REACTIVE_POWER_PHASE_1,
                "position": 12,
                "has_scaling_factor": True,
                "unit_str": "W",
                "description_str": "Power (vendor specific)",
                "sensor_class": EmuReactivePowerSensor,
            },
            {
                "name": REACTIVE_POWER_PHASE_2,
                "position": 13,
                "has_scaling_factor": True,
                "unit_str": "W",
                "description_str": "Power (vendor specific)",
                "sensor_class": EmuReactivePowerSensor,
            },
            {
                "name": REACTIVE_POWER_PHASE_3,
                "position": 14,
                "has_scaling_factor": True,
                "unit_str": "W",
                "description_str": "Power (vendor specific)",
                "sensor_class": EmuReactivePowerSensor,
            },
            {
                "name": REACTIVE_POWER_ALL_PHASES,
                "position": 15,
                "has_scaling_factor": True,
                "unit_str": "W",
                "description_str": "Power",
                "sensor_class": EmuReactivePowerSensor,
            },
            {
                "name": APPARENT_POWER_ALL_PHASES,
                "position": 16,
                "has_scaling_factor": True,
                "unit_str": "W",
                "description_str": "Power",
                "sensor_class": EmuApparentPowerSensor,
            },
            {
                "name": VOLTAGE_PHASE_1,
                "position": 17,
                "has_scaling_factor": True,
                "unit_str": "V",
                "description_str": "Volts (vendor specific)",
                "sensor_class": EmuVoltageSensor,
            },
            {
                "name": VOLTAGE_PHASE_2,
                "position": 18,
                "has_scaling_factor": True,
                "unit_str": "V",
                "description_str": "Volts (vendor specific)",
                "sensor_class": EmuVoltageSensor,
            },
            {
                "name": VOLTAGE_PHASE_3,
                "position": 19,
                "has_scaling_factor": True,
                "unit_str": "V",
                "description_str": "Volts (vendor specific)",
                "sensor_class": EmuVoltageSensor,
            },
            {
                "name": CURRENT_PHASE_1,
                "position": 20,
                "has_scaling_factor": True,
                "unit_str": "A",
                "description_str": "Ampere (vendor specific)",
                "sensor_class": EmuCurrentSensor,
            },
            {
                "name": CURRENT_PHASE_2,
                "position": 21,
                "has_scaling_factor": True,
                "unit_str": "A",
                "description_str": "Ampere (vendor specific)",
                "sensor_class": EmuCurrentSensor,
            },
            {
                "name": CURRENT_PHASE_3,
                "position": 22,
                "has_scaling_factor": True,
                "unit_str": "A",
                "description_str": "Ampere (vendor specific)",
                "sensor_class": EmuCurrentSensor,
            },
            {
                "name": CURRENT_ALL_PHASES,
                "position": 23,
                "has_scaling_factor": True,
                "unit_str": "A",
                "description_str": "Ampere",
                "sensor_class": EmuCurrentSensor,
            },
            {
                "name": FORM_FACTOR_PHASE_1,
                "position": 24,
                "has_scaling_factor": False,
                "unit_str": "None",
                "description_str": "Special supplier information",
                "sensor_class": EmuFormFactorSensor,
            },
            {
                "name": FORM_FACTOR_PHASE_2,
                "position": 25,
                "has_scaling_factor": False,
                "unit_str": "None",
                "description_str": "Special supplier information",
                "sensor_class": EmuFormFactorSensor,
            },
            {
                "name": FORM_FACTOR_PHASE_3,
                "position": 26,
                "has_scaling_factor": False,
                "unit_str": "None",
                "description_str": "Special supplier information",
                "sensor_class": EmuFormFactorSensor,
            },
            {
                "name": FREQUENCY,
                "position": 27,
                "has_scaling_factor": True,
                "unit_str": "None",
                "description_str": "Special supplier information",
                "sensor_class": EmuFrequencySensor,
            },
            {
                "name": POWER_FAILURES,
                "position": 28,
                "has_scaling_factor": False,
                "unit_str": "None",
                "description_str": "Reset counter",
                "sensor_class": EmuPowerFailureSensor,
            },
            {
                "name": CURRENT_TRANSFORMER_FACTOR,
                "position": 29,
                "has_scaling_factor": True,
                "unit_str": "None",
                "description_str": "Special supplier information",
                "sensor_class": EmuTransformerFactorSensor,
            },
            {
                "name": ERROR_FLAGS,
                "position": 30,
                "has_scaling_factor": False,
                "unit_str": "Bin",
                "description_str": "Error flags (Device type specific)",
                "sensor_class": EmuErrorSensor,
            },
        ]

    @property
    def version_number(self) -> int:
        """Get the Version number of this device."""
        return 16

    @property
    def sensor_count(self) -> int:
        """Get the sensor count."""
        return 31

    @property
    def model_name(self) -> str:
        """Get the model name."""
        return "Professional 3/75"

    @property
    def manufacturer_name(self) -> str:
        """Get the manufacturer name."""
        return "EMU"
