import logging

from homeassistant.core import HomeAssistant

from custom_components.emu_m_bus_center.const import (
    ERROR_FLAGS,
    VOLTAGE,
    CURRENT,
    FORM_FACTOR,
    ACTIVE_POWER,
    FREQUENCY,
    ACTIVE_ENERGY_IMPORT,
    ACTIVE_ENERGY_IMPORT_RESETTABLE,
    SERIAL_NO,
)
from custom_components.emu_m_bus_center.sensor import (
    EmuActiveEnergySensor,
    EmuActivePowerSensor,
    EmuVoltageSensor,
    EmuCurrentSensor,
    EmuErrorSensor,
    EmuCoordinator,
    EmuFormFactorSensor,
    EmuFrequencySensor,
    EmuActiveEnergyResettableSensor,
    EmuSerialNoSensor,
)


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

    def sensors(self) -> list[str]:
        return [
            EmuVoltageSensor(self, VOLTAGE),
            EmuCurrentSensor(self, CURRENT),
            EmuFormFactorSensor(self, FORM_FACTOR),
            EmuActivePowerSensor(self, ACTIVE_POWER),
            EmuFrequencySensor(self, FREQUENCY),
            EmuActiveEnergySensor(self, ACTIVE_ENERGY_IMPORT),
            EmuActiveEnergyResettableSensor(self, ACTIVE_ENERGY_IMPORT_RESETTABLE),
            EmuSerialNoSensor(self, SERIAL_NO),
            EmuErrorSensor(self, ERROR_FLAGS),
        ]

    def parse(self, data: str) -> dict[str, float]:
        voltage = next(item for item in data if item["Position"] == 0)
        # test if we found the right entry voltage
        if not (
            voltage["UnitStr"] == "V"
            and voltage["DescriptionStr"] == "Volts (vendor specific)"
        ):
            raise ValueError(
                "Did not find the required Fields for voltage in the JSON response from the "
                "M-Bus Center"
            )

        current = next(item for item in data if item["Position"] == 1)
        # test if we found the right entry current
        if not (
            current["UnitStr"] == "A"
            and current["DescriptionStr"] == "Ampere (vendor specific)"
        ):
            raise ValueError(
                "Did not find the required Fields for current in the JSON response from the "
                "M-Bus Center"
            )
        form_factor = next(item for item in data if item["Position"] == 2)
        # test if we found the right entry for form_factor
        if not (
            form_factor["UnitStr"] == "None"
            and form_factor["DescriptionStr"] == "Special supplier information"
        ):
            raise ValueError(
                "Did not find the required Fields for form_factor in the JSON response from the "
                "M-Bus Center"
            )
        active_power = next(item for item in data if item["Position"] == 3)
        # test if we found the right entry for active_power
        if not (
            active_power["UnitStr"] == "W" and active_power["DescriptionStr"] == "Power"
        ):
            raise ValueError(
                "Did not find the required Fields for active_power in the JSON response from the "
                "M-Bus Center"
            )

        active_energy_import = next(item for item in data if item["Position"] == 5)
        # test if we found the right entry for active_energy_import
        if not (
            active_energy_import["UnitStr"] == "Wh"
            and active_energy_import["DescriptionStr"] == "Energy"
        ):
            raise ValueError(
                "Did not find the required Fields for active_energy_import in the JSON response from the "
                "M-Bus Center"
            )

        active_energy_import_resettable = next(
            item for item in data if item["Position"] == 5
        )
        # test if we found the right entry for active_energy_import_resettable
        if not (
            active_energy_import_resettable["UnitStr"] == "Wh"
            and active_energy_import_resettable["DescriptionStr"] == "Energy"
        ):
            raise ValueError(
                "Did not find the required Fields for active_energy_import_resettable in the JSON response from the "
                "M-Bus Center"
            )

        serial_no = next(item for item in data if item["Position"] == 7)
        # test if we found the right entry for serial_no
        if not (serial_no["UnitStr"] == "None"):
            raise ValueError(
                "Did not find the required Fields for serial_no in the JSON response from the "
                "M-Bus Center"
            )

        error_flags = next(item for item in data if item["Position"] == 12)
        # test if we found the right entry error_flags
        if not (
            error_flags["UnitStr"] == "Bin"
            and error_flags["DescriptionStr"] == "Error flags (Device type specific)"
        ):
            raise ValueError(
                "Did not find the required Fields for error_flags in the JSON response from the "
                "M-Bus Center"
            )

        return {
            VOLTAGE: int(voltage["LoggerLastValue"])
            / (voltage.get("CfgFactor", 1) if voltage.get("CfgFactor", 1) != 0 else 1),
            CURRENT: int(current["LoggerLastValue"])
            / (current.get("CfgFactor", 1) if current.get("CfgFactor", 1) != 0 else 1),
            FORM_FACTOR: int(form_factor["LoggerLastValue"])
            / (
                form_factor.get("CfgFactor", 1)
                if form_factor.get("CfgFactor", 1) != 0
                else 1
            ),
            ACTIVE_POWER: int(active_power["LoggerLastValue"])
            / (
                active_power.get("CfgFactor", 1)
                if active_power.get("CfgFactor", 1) != 0
                else 1
            ),
            ACTIVE_ENERGY_IMPORT: int(active_energy_import["LoggerLastValue"])
            / (
                active_energy_import.get("CfgFactor", 1)
                if active_energy_import.get("CfgFactor", 1) != 0
                else 1
            ),
            ACTIVE_ENERGY_IMPORT_RESETTABLE: int(
                active_energy_import_resettable["LoggerLastValue"]
            )
            / (
                active_energy_import_resettable.get("CfgFactor", 1)
                if active_energy_import_resettable.get("CfgFactor", 1) != 0
                else 1
            ),
            SERIAL_NO: int(serial_no["LoggerLastValue"]),
            ERROR_FLAGS: int(error_flags["LoggerLastValue"]),
        }
