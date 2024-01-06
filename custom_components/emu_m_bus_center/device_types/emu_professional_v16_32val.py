import logging

from custom_components.emu_m_bus_center.const import ACTIVE_ENERGY_EXPORT_TARIFF_1
from custom_components.emu_m_bus_center.const import ACTIVE_ENERGY_EXPORT_TARIFF_2
from custom_components.emu_m_bus_center.const import ACTIVE_ENERGY_IMPORT_TARIFF_1
from custom_components.emu_m_bus_center.const import ACTIVE_ENERGY_IMPORT_TARIFF_2
from custom_components.emu_m_bus_center.const import ACTIVE_POWER_ALL_PHASES
from custom_components.emu_m_bus_center.const import ACTIVE_POWER_PHASE_1
from custom_components.emu_m_bus_center.const import ACTIVE_POWER_PHASE_2
from custom_components.emu_m_bus_center.const import ACTIVE_POWER_PHASE_3
from custom_components.emu_m_bus_center.const import APPARENT_POWER_ALL_PHASES
from custom_components.emu_m_bus_center.const import CURRENT_ALL_PHASES
from custom_components.emu_m_bus_center.const import CURRENT_PHASE_1
from custom_components.emu_m_bus_center.const import CURRENT_PHASE_2
from custom_components.emu_m_bus_center.const import CURRENT_PHASE_3
from custom_components.emu_m_bus_center.const import CURRENT_TRANSFORMER_FACTOR
from custom_components.emu_m_bus_center.const import ERROR_FLAGS
from custom_components.emu_m_bus_center.const import FORM_FACTOR_PHASE_1
from custom_components.emu_m_bus_center.const import FORM_FACTOR_PHASE_2
from custom_components.emu_m_bus_center.const import FORM_FACTOR_PHASE_3
from custom_components.emu_m_bus_center.const import FREQUENCY
from custom_components.emu_m_bus_center.const import POWER_FAILURES
from custom_components.emu_m_bus_center.const import REACTIVE_ENERGY_CAPACITIVE_TARIFF_1
from custom_components.emu_m_bus_center.const import REACTIVE_ENERGY_CAPACITIVE_TARIFF_2
from custom_components.emu_m_bus_center.const import REACTIVE_ENERGY_INDUCTIVE_TARIFF_1
from custom_components.emu_m_bus_center.const import REACTIVE_ENERGY_INDUCTIVE_TARIFF_2
from custom_components.emu_m_bus_center.const import REACTIVE_POWER_ALL_PHASES
from custom_components.emu_m_bus_center.const import REACTIVE_POWER_PHASE_1
from custom_components.emu_m_bus_center.const import REACTIVE_POWER_PHASE_2
from custom_components.emu_m_bus_center.const import REACTIVE_POWER_PHASE_3
from custom_components.emu_m_bus_center.const import SERIAL_NO
from custom_components.emu_m_bus_center.const import VOLTAGE_PHASE_1
from custom_components.emu_m_bus_center.const import VOLTAGE_PHASE_2
from custom_components.emu_m_bus_center.const import VOLTAGE_PHASE_3
from custom_components.emu_m_bus_center.sensor import EmuActiveEnergySensor
from custom_components.emu_m_bus_center.sensor import EmuActivePowerSensor
from custom_components.emu_m_bus_center.sensor import EmuApparentPowerSensor
from custom_components.emu_m_bus_center.sensor import EmuBaseSensor
from custom_components.emu_m_bus_center.sensor import EmuCoordinator
from custom_components.emu_m_bus_center.sensor import EmuCurrentSensor
from custom_components.emu_m_bus_center.sensor import EmuErrorSensor
from custom_components.emu_m_bus_center.sensor import EmuFormFactorSensor
from custom_components.emu_m_bus_center.sensor import EmuFrequencySensor
from custom_components.emu_m_bus_center.sensor import EmuPowerFailureSensor
from custom_components.emu_m_bus_center.sensor import EmuReactiveEnergySensor
from custom_components.emu_m_bus_center.sensor import EmuReactivePowerSensor
from custom_components.emu_m_bus_center.sensor import EmuSerialNoSensor
from custom_components.emu_m_bus_center.sensor import EmuTransformerFactorSensor
from custom_components.emu_m_bus_center.sensor import EmuVoltageSensor
from homeassistant.core import HomeAssistant


class EmuProfessionalV16_32val(EmuCoordinator):
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
        return 16

    @property
    def sensor_count(self) -> int:
        return 32

    @property
    def model_name(self) -> str:
        return "Professional II 3/100"

    @property
    def manufacturer_name(self) -> str:
        return "EMU"

    def sensors(self) -> list[EmuBaseSensor]:
        return [
            EmuSerialNoSensor(self, SERIAL_NO),
            EmuActiveEnergySensor(self, ACTIVE_ENERGY_IMPORT_TARIFF_1),
            EmuActiveEnergySensor(self, ACTIVE_ENERGY_IMPORT_TARIFF_2),
            EmuActiveEnergySensor(self, ACTIVE_ENERGY_EXPORT_TARIFF_1),
            EmuActiveEnergySensor(self, ACTIVE_ENERGY_EXPORT_TARIFF_2),
            EmuReactiveEnergySensor(self, REACTIVE_ENERGY_INDUCTIVE_TARIFF_1),
            EmuReactiveEnergySensor(self, REACTIVE_ENERGY_INDUCTIVE_TARIFF_2),
            EmuReactiveEnergySensor(self, REACTIVE_ENERGY_CAPACITIVE_TARIFF_1),
            EmuReactiveEnergySensor(self, REACTIVE_ENERGY_CAPACITIVE_TARIFF_2),
            EmuActivePowerSensor(self, ACTIVE_POWER_PHASE_1),
            EmuActivePowerSensor(self, ACTIVE_POWER_PHASE_2),
            EmuActivePowerSensor(self, ACTIVE_POWER_PHASE_3),
            EmuActivePowerSensor(self, ACTIVE_POWER_ALL_PHASES),
            EmuReactivePowerSensor(self, REACTIVE_POWER_PHASE_1),
            EmuReactivePowerSensor(self, REACTIVE_POWER_PHASE_2),
            EmuReactivePowerSensor(self, REACTIVE_POWER_PHASE_3),
            EmuReactivePowerSensor(self, REACTIVE_POWER_ALL_PHASES),
            EmuApparentPowerSensor(self, APPARENT_POWER_ALL_PHASES),
            EmuVoltageSensor(self, VOLTAGE_PHASE_1),
            EmuVoltageSensor(self, VOLTAGE_PHASE_2),
            EmuVoltageSensor(self, VOLTAGE_PHASE_3),
            EmuCurrentSensor(self, CURRENT_PHASE_1),
            EmuCurrentSensor(self, CURRENT_PHASE_2),
            EmuCurrentSensor(self, CURRENT_PHASE_3),
            EmuCurrentSensor(self, CURRENT_ALL_PHASES),
            EmuFormFactorSensor(self, FORM_FACTOR_PHASE_1),
            EmuFormFactorSensor(self, FORM_FACTOR_PHASE_2),
            EmuFormFactorSensor(self, FORM_FACTOR_PHASE_3),
            EmuFrequencySensor(self, FREQUENCY),
            EmuPowerFailureSensor(self, POWER_FAILURES),
            EmuTransformerFactorSensor(self, CURRENT_TRANSFORMER_FACTOR),
            EmuErrorSensor(self, ERROR_FLAGS),
        ]

    def parse(self, data: list[dict]) -> dict[str, float]:
        serial_no = next(item for item in data if item["Position"] == 0)
        # test if we found the right entry for serial_no
        if not (serial_no["UnitStr"] == "None"):
            raise ValueError(
                "Did not find the required Fields for serial_no in the JSON response from the "
                "M-Bus Center"
            )
        active_energy_import_tariff_1 = next(
            item for item in data if item["Position"] == 1
        )
        # test if we found the right entry for active_energy_import_tariff_1
        if not (
            active_energy_import_tariff_1["UnitStr"] == "Wh"
            and active_energy_import_tariff_1["DescriptionStr"] == "Energy"
        ):
            raise ValueError(
                "Did not find the required Fields for active_energy_import_tariff_1 in the JSON response from the "
                "M-Bus Center"
            )

        active_energy_import_tariff_2 = next(
            item for item in data if item["Position"] == 2
        )
        # test if we found the right entry for active_energy_import_tariff_2
        if not (
            active_energy_import_tariff_2["UnitStr"] == "Wh"
            and active_energy_import_tariff_2["DescriptionStr"] == "Energy"
        ):
            raise ValueError(
                "Did not find the required Fields for active_energy_import_tariff_2 in the JSON response from the "
                "M-Bus Center"
            )

        reactive_energy_inductive_tariff_1 = next(
            item for item in data if item["Position"] == 3
        )
        # test if we found the right entry for reactive_energy_inductive_tariff_1
        if not (
            reactive_energy_inductive_tariff_1["UnitStr"] == "Wh"
            and reactive_energy_inductive_tariff_1["DescriptionStr"] == "Energy"
        ):
            raise ValueError(
                "Did not find the required Fields for reactive_energy_inductive_tariff_1 in the JSON response from the "
                "M-Bus Center"
            )

        reactive_energy_inductive_tariff_2 = next(
            item for item in data if item["Position"] == 4
        )
        # test if we found the right entry for reactive_energy_inductive_tariff_2
        if not (
            reactive_energy_inductive_tariff_2["UnitStr"] == "Wh"
            and reactive_energy_inductive_tariff_2["DescriptionStr"] == "Energy"
        ):
            raise ValueError(
                "Did not find the required Fields for reactive_energy_inductive_tariff_2 in the JSON response from the "
                "M-Bus Center"
            )

        active_power_phase_1 = next(item for item in data if item["Position"] == 5)
        # test if we found the right entry for active_power_phase_1
        if not (
            active_power_phase_1["UnitStr"] == "W"
            and active_power_phase_1["DescriptionStr"] == "Power (vendor specific)"
        ):
            raise ValueError(
                "Did not find the required Fields for active_power_phase_1 in the JSON response from the "
                "M-Bus Center"
            )

        active_power_phase_2 = next(item for item in data if item["Position"] == 6)
        # test if we found the right entry for active_power_phase_2
        if not (
            active_power_phase_2["UnitStr"] == "W"
            and active_power_phase_2["DescriptionStr"] == "Power (vendor specific)"
        ):
            raise ValueError(
                "Did not find the required Fields for active_power_phase_2 in the JSON response from the "
                "M-Bus Center"
            )

        active_power_phase_3 = next(item for item in data if item["Position"] == 7)
        # test if we found the right entry for active_power_phase_3
        if not (
            active_power_phase_3["UnitStr"] == "W"
            and active_power_phase_3["DescriptionStr"] == "Power (vendor specific)"
        ):
            raise ValueError(
                "Did not find the required Fields for active_power_phase_3 in the JSON response from the "
                "M-Bus Center"
            )

        active_power_all_phases = next(item for item in data if item["Position"] == 8)
        # test if we found the right entry for active_power_all_phases
        if not (
            active_power_all_phases["UnitStr"] == "W"
            and active_power_all_phases["DescriptionStr"] == "Power"
        ):
            raise ValueError(
                "Did not find the required Fields for active_power_all_phases in the JSON response from the "
                "M-Bus Center"
            )

        reactive_power_phase_1 = next(item for item in data if item["Position"] == 9)
        # test if we found the right entry for reactive_power_phase_1
        if not (
            reactive_power_phase_1["UnitStr"] == "W"
            and reactive_power_phase_1["DescriptionStr"] == "Power (vendor specific)"
        ):
            raise ValueError(
                "Did not find the required Fields for reactive_power_phase_1 in the JSON response from the "
                "M-Bus Center"
            )

        reactive_power_phase_2 = next(item for item in data if item["Position"] == 10)
        # test if we found the right entry for reactive_power_phase_2
        if not (
            reactive_power_phase_2["UnitStr"] == "W"
            and reactive_power_phase_2["DescriptionStr"] == "Power (vendor specific)"
        ):
            raise ValueError(
                "Did not find the required Fields for reactive_power_phase_2 in the JSON response from the "
                "M-Bus Center"
            )

        reactive_power_phase_3 = next(item for item in data if item["Position"] == 11)
        # test if we found the right entry for reactive_power_phase_3
        if not (
            reactive_power_phase_3["UnitStr"] == "W"
            and reactive_power_phase_3["DescriptionStr"] == "Power (vendor specific)"
        ):
            raise ValueError(
                "Did not find the required Fields for reactive_power_phase_3 in the JSON response from the "
                "M-Bus Center"
            )

        reactive_power_all_phases = next(
            item for item in data if item["Position"] == 12
        )
        # test if we found the right entry for reactive_power_all_phases
        if not (
            reactive_power_all_phases["UnitStr"] == "W"
            and reactive_power_all_phases["DescriptionStr"] == "Power"
        ):
            raise ValueError(
                "Did not find the required Fields for reactive_power_all_phases in the JSON response from the "
                "M-Bus Center"
            )

        voltage_phase_1 = next(item for item in data if item["Position"] == 13)
        # test if we found the right entry voltage_phase_1
        if not (
            voltage_phase_1["UnitStr"] == "V"
            and voltage_phase_1["DescriptionStr"] == "Volts (vendor specific)"
        ):
            raise ValueError(
                "Did not find the required Fields for voltage_phase_1 in the JSON response from the "
                "M-Bus Center"
            )

        voltage_phase_2 = next(item for item in data if item["Position"] == 14)
        # test if we found the right entry voltage_phase_2
        if not (
            voltage_phase_2["UnitStr"] == "V"
            and voltage_phase_2["DescriptionStr"] == "Volts (vendor specific)"
        ):
            raise ValueError(
                "Did not find the required Fields for voltage_phase_2 in the JSON response from the "
                "M-Bus Center"
            )

        voltage_phase_3 = next(item for item in data if item["Position"] == 15)
        # test if we found the right entry voltage_phase_3
        if not (
            voltage_phase_3["UnitStr"] == "V"
            and voltage_phase_3["DescriptionStr"] == "Volts (vendor specific)"
        ):
            raise ValueError(
                "Did not find the required Fields for voltage_phase_3 in the JSON response from the "
                "M-Bus Center"
            )

        current_phase_1 = next(item for item in data if item["Position"] == 22)
        # test if we found the right entry current_phase_1
        if not (
            current_phase_1["UnitStr"] == "A"
            and current_phase_1["DescriptionStr"] == "Ampere (vendor specific)"
        ):
            raise ValueError(
                "Did not find the required Fields for current_phase_1 in the JSON response from the "
                "M-Bus Center"
            )

        current_phase_2 = next(item for item in data if item["Position"] == 23)
        # test if we found the right entry current_phase_2
        if not (
            current_phase_2["UnitStr"] == "A"
            and current_phase_2["DescriptionStr"] == "Ampere (vendor specific)"
        ):
            raise ValueError(
                "Did not find the required Fields for current_phase_2 in the JSON response from the "
                "M-Bus Center"
            )

        current_phase_3 = next(item for item in data if item["Position"] == 24)
        # test if we found the right entry current_phase_3
        if not (
            current_phase_3["UnitStr"] == "A"
            and current_phase_3["DescriptionStr"] == "Ampere (vendor specific)"
        ):
            raise ValueError(
                "Did not find the required Fields for current_phase_3 in the JSON response from the "
                "M-Bus Center"
            )

        current_all_phases = next(item for item in data if item["Position"] == 25)
        # test if we found the right entry current_all_phases
        if not (
            current_all_phases["UnitStr"] == "A"
            and current_all_phases["DescriptionStr"] == "Ampere"
        ):
            raise ValueError(
                "Did not find the required Fields for current_all_phases in the JSON response from the "
                "M-Bus Center"
            )

        form_factor_phase_1 = next(item for item in data if item["Position"] == 26)
        # test if we found the right entry for form_factor_phase_1
        if not (
            form_factor_phase_1["UnitStr"] == "None"
            and form_factor_phase_1["DescriptionStr"] == "Special supplier information"
        ):
            raise ValueError(
                "Did not find the required Fields for form_factor_phase_1 in the JSON response from the "
                "M-Bus Center"
            )

        form_factor_phase_2 = next(item for item in data if item["Position"] == 27)
        # test if we found the right entry for form_factor_phase_2
        if not (
            form_factor_phase_2["UnitStr"] == "None"
            and form_factor_phase_2["DescriptionStr"] == "Special supplier information"
        ):
            raise ValueError(
                "Did not find the required Fields for form_factor_phase_2 in the JSON response from the "
                "M-Bus Center"
            )

        form_factor_phase_3 = next(item for item in data if item["Position"] == 28)
        # test if we found the right entry for form_factor_phase_3
        if not (
            form_factor_phase_3["UnitStr"] == "None"
            and form_factor_phase_3["DescriptionStr"] == "Special supplier information"
        ):
            raise ValueError(
                "Did not find the required Fields for form_factor_phase_3 in the JSON response from the "
                "M-Bus Center"
            )

        frequency = next(item for item in data if item["Position"] == 29)
        # test if we found the right entry frequency
        if not (
            (frequency["UnitStr"] == "None" or frequency["UnitStr"] == "Hz")
            and frequency["DescriptionStr"] == "Special supplier information"
        ):
            raise ValueError(
                "Did not find the required Fields for frequency in the JSON response from the "
                "M-Bus Center"
            )

        power_failures = next(item for item in data if item["Position"] == 30)
        # test if we found the right entry power_failures
        if not (
            power_failures["UnitStr"] == "None"
            and power_failures["DescriptionStr"] == "Reset counter"
        ):
            raise ValueError(
                "Did not find the required Fields for resets in the JSON response from the "
                "M-Bus Center"
            )

        error_flags = next(item for item in data if item["Position"] == 31)
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
            SERIAL_NO: serial_no["LoggerLastValue"],
            ACTIVE_ENERGY_IMPORT_TARIFF_1: int(
                active_energy_import_tariff_1["LoggerLastValue"]
            )
            / (
                active_energy_import_tariff_1.get("CfgFactor", 1)
                if active_energy_import_tariff_1.get("CfgFactor", 1) != 0
                else 1
            ),
            ACTIVE_ENERGY_IMPORT_TARIFF_2: int(
                active_energy_import_tariff_2["LoggerLastValue"]
            )
            / (
                active_energy_import_tariff_2.get("CfgFactor", 1)
                if active_energy_import_tariff_2.get("CfgFactor", 1) != 0
                else 1
            ),
            REACTIVE_ENERGY_INDUCTIVE_TARIFF_1: int(
                reactive_energy_inductive_tariff_1["LoggerLastValue"]
            )
            / (
                reactive_energy_inductive_tariff_1.get("CfgFactor", 1)
                if reactive_energy_inductive_tariff_1.get("CfgFactor", 1) != 0
                else 1
            ),
            REACTIVE_ENERGY_INDUCTIVE_TARIFF_2: int(
                reactive_energy_inductive_tariff_2["LoggerLastValue"]
            )
            / (
                reactive_energy_inductive_tariff_2.get("CfgFactor", 1)
                if reactive_energy_inductive_tariff_2.get("CfgFactor", 1) != 0
                else 1
            ),
            ACTIVE_POWER_PHASE_1: int(active_power_phase_1["LoggerLastValue"])
            / (
                active_power_phase_1.get("CfgFactor", 1)
                if active_power_phase_1.get("CfgFactor", 1) != 0
                else 1
            ),
            ACTIVE_POWER_PHASE_2: int(active_power_phase_2["LoggerLastValue"])
            / (
                active_power_phase_2.get("CfgFactor", 1)
                if active_power_phase_2.get("CfgFactor", 1) != 0
                else 1
            ),
            ACTIVE_POWER_PHASE_3: int(active_power_phase_3["LoggerLastValue"])
            / (
                active_power_phase_3.get("CfgFactor", 1)
                if active_power_phase_3.get("CfgFactor", 1) != 0
                else 1
            ),
            ACTIVE_POWER_ALL_PHASES: int(active_power_all_phases["LoggerLastValue"])
            / (
                active_power_all_phases.get("CfgFactor", 1)
                if active_power_all_phases.get("CfgFactor", 1) != 0
                else 1
            ),
            REACTIVE_POWER_PHASE_1: int(reactive_power_phase_1["LoggerLastValue"])
            / (
                reactive_power_phase_1.get("CfgFactor", 1)
                if reactive_power_phase_1.get("CfgFactor", 1) != 0
                else 1
            ),
            REACTIVE_POWER_PHASE_2: int(reactive_power_phase_2["LoggerLastValue"])
            / (
                reactive_power_phase_2.get("CfgFactor", 1)
                if reactive_power_phase_2.get("CfgFactor", 1) != 0
                else 1
            ),
            REACTIVE_POWER_PHASE_3: int(reactive_power_phase_3["LoggerLastValue"])
            / (
                reactive_power_phase_3.get("CfgFactor", 1)
                if reactive_power_phase_3.get("CfgFactor", 1) != 0
                else 1
            ),
            REACTIVE_POWER_ALL_PHASES: int(reactive_power_all_phases["LoggerLastValue"])
            / (
                reactive_power_all_phases.get("CfgFactor", 1)
                if reactive_power_all_phases.get("CfgFactor", 1) != 0
                else 1
            ),
            VOLTAGE_PHASE_1: int(voltage_phase_1["LoggerLastValue"])
            / (
                voltage_phase_1.get("CfgFactor", 1)
                if voltage_phase_1.get("CfgFactor", 1) != 0
                else 1
            ),
            VOLTAGE_PHASE_2: int(voltage_phase_2["LoggerLastValue"])
            / (
                voltage_phase_2.get("CfgFactor", 1)
                if voltage_phase_2.get("CfgFactor", 1) != 0
                else 1
            ),
            VOLTAGE_PHASE_3: int(voltage_phase_3["LoggerLastValue"])
            / (
                voltage_phase_3.get("CfgFactor", 1)
                if voltage_phase_3.get("CfgFactor", 1) != 0
                else 1
            ),
            CURRENT_PHASE_1: int(current_phase_1["LoggerLastValue"])
            / (
                current_phase_1.get("CfgFactor", 1)
                if current_phase_1.get("CfgFactor", 1) != 0
                else 1
            ),
            CURRENT_PHASE_2: int(current_phase_2["LoggerLastValue"])
            / (
                current_phase_2.get("CfgFactor", 1)
                if current_phase_2.get("CfgFactor", 1) != 0
                else 1
            ),
            CURRENT_PHASE_3: int(current_phase_3["LoggerLastValue"])
            / (
                current_phase_3.get("CfgFactor", 1)
                if current_phase_3.get("CfgFactor", 1) != 0
                else 1
            ),
            CURRENT_ALL_PHASES: int(current_all_phases["LoggerLastValue"])
            / (
                current_all_phases.get("CfgFactor", 1)
                if current_all_phases.get("CfgFactor", 1) != 0
                else 1
            ),
            FORM_FACTOR_PHASE_1: int(form_factor_phase_1["LoggerLastValue"])
            / (
                form_factor_phase_1.get("CfgFactor", 1)
                if form_factor_phase_1.get("CfgFactor", 1) != 0
                else 1
            ),
            FORM_FACTOR_PHASE_2: int(form_factor_phase_2["LoggerLastValue"])
            / (
                form_factor_phase_2.get("CfgFactor", 1)
                if form_factor_phase_2.get("CfgFactor", 1) != 0
                else 1
            ),
            FORM_FACTOR_PHASE_3: int(form_factor_phase_3["LoggerLastValue"])
            / (
                form_factor_phase_3.get("CfgFactor", 1)
                if form_factor_phase_3.get("CfgFactor", 1) != 0
                else 1
            ),
            FREQUENCY: int(frequency["LoggerLastValue"])
            / (
                frequency.get("CfgFactor", 1)
                if frequency.get("CfgFactor", 1) != 0
                else 1
            ),
            POWER_FAILURES: int(power_failures["LoggerLastValue"])
            / (
                power_failures.get("CfgFactor", 1)
                if power_failures.get("CfgFactor", 1) != 0
                else 1
            ),
            ERROR_FLAGS: int(error_flags["LoggerLastValue"]),
        }
