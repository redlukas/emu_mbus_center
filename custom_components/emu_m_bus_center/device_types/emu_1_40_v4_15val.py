import logging

from custom_components.emu_m_bus_center.const import ACTIVE_ENERGY_IMPORT
from custom_components.emu_m_bus_center.const import ACTIVE_ENERGY_IMPORT_RESETTABLE
from custom_components.emu_m_bus_center.const import ACTIVE_POWER
from custom_components.emu_m_bus_center.const import CURRENT
from custom_components.emu_m_bus_center.const import ERROR_FLAGS
from custom_components.emu_m_bus_center.const import FORM_FACTOR
from custom_components.emu_m_bus_center.const import FREQUENCY
from custom_components.emu_m_bus_center.const import SERIAL_NO
from custom_components.emu_m_bus_center.const import VOLTAGE
from custom_components.emu_m_bus_center.sensor import EmuActiveEnergyResettableSensor
from custom_components.emu_m_bus_center.sensor import EmuActiveEnergySensor
from custom_components.emu_m_bus_center.sensor import EmuActivePowerSensor
from custom_components.emu_m_bus_center.sensor import EmuCoordinator
from custom_components.emu_m_bus_center.sensor import EmuCurrentSensor
from custom_components.emu_m_bus_center.sensor import EmuErrorSensor
from custom_components.emu_m_bus_center.sensor import EmuFormFactorSensor
from custom_components.emu_m_bus_center.sensor import EmuFrequencySensor
from custom_components.emu_m_bus_center.sensor import EmuSerialNoSensor
from custom_components.emu_m_bus_center.sensor import EmuVoltageSensor
from homeassistant.core import HomeAssistant


class Emu_1_40_V4_15val(EmuCoordinator):
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
        return 4

    @property
    def sensor_count(self) -> int:
        return 15

    @property
    def model_name(self) -> str:
        return "1/40"

    @property
    def manufacturer_name(self) -> str:
        return "EMU"
