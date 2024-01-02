from custom_components.emu_m_bus_center.const import (
    ACTIVE_ENERGY_TARIFF_1,
    ACTIVE_ENERGY_TARIFF_2,
    ACTIVE_POWER_PHASE_1,
    ACTIVE_POWER_PHASE_2,
    ACTIVE_POWER_PHASE_3,
    ACTIVE_POWER_ALL_PHASES,
    VOLTAGE_PHASE_1,
    VOLTAGE_PHASE_2,
    VOLTAGE_PHASE_3,
    CURRENT_PHASE_1,
    CURRENT_PHASE_2,
    CURRENT_PHASE_3,
    CURRENT_ALL_PHASES,
    FREQUENCY,
    RESET_COUNTER,
    CURRENT_TRANSFORMER_FACTOR,
    ERROR_FLAGS,
)
from custom_components.emu_m_bus_center.device_types.readable_device import (
    Readable_device,
)
from custom_components.emu_m_bus_center.sensor import (
    EmuEnergySensor,
    EmuPowerSensor,
    EmuVoltageSensor,
    EmuCurrentSensor,
    EmuFrequencySensor,
    EmuResetSensor,
    EmuTransformerFactorSensor,
    EmuErrorSensor,
)


class EmuAllrounderV16_17val(Readable_device):
    @property
    def version_number(self):
        return 16

    @property
    def sensor_count(self):
        return 17

    @property
    def model_name(self) -> str:
        return "Allrounder 3/75"

    @property
    def manufacturer_name(self) -> str:
        return "EMU"

    def sensors(self, coordinator) -> list[str]:
        return [
            EmuEnergySensor(coordinator, ACTIVE_ENERGY_TARIFF_1),
            EmuEnergySensor(coordinator, ACTIVE_ENERGY_TARIFF_2),
            EmuPowerSensor(coordinator, ACTIVE_POWER_PHASE_1),
            EmuPowerSensor(coordinator, ACTIVE_POWER_PHASE_2),
            EmuPowerSensor(coordinator, ACTIVE_POWER_PHASE_3),
            EmuPowerSensor(coordinator, ACTIVE_POWER_ALL_PHASES),
            EmuVoltageSensor(coordinator, VOLTAGE_PHASE_1),
            EmuVoltageSensor(coordinator, VOLTAGE_PHASE_2),
            EmuVoltageSensor(coordinator, VOLTAGE_PHASE_3),
            EmuCurrentSensor(coordinator, CURRENT_PHASE_1),
            EmuCurrentSensor(coordinator, CURRENT_PHASE_2),
            EmuCurrentSensor(coordinator, CURRENT_PHASE_3),
            EmuCurrentSensor(coordinator, CURRENT_ALL_PHASES),
            EmuFrequencySensor(coordinator, FREQUENCY),
            EmuResetSensor(coordinator, RESET_COUNTER),
            EmuTransformerFactorSensor(coordinator, CURRENT_TRANSFORMER_FACTOR),
            EmuErrorSensor(coordinator, ERROR_FLAGS),
        ]

    def parse(self, data: str) -> dict[str, float]:
        active_energy_tariff_1 = next(item for item in data if item["Position"] == 0)
        # test if we found the right entry for active_energy_tariff_1
        if not (
            active_energy_tariff_1["UnitStr"] == "Wh"
            and active_energy_tariff_1["DescriptionStr"] == "Energy"
        ):
            raise ValueError(
                "Did not find the required Fields for active_energy_tariff_1 in the JSON response from the "
                "M-Bus Center"
            )

        active_energy_tariff_2 = next(item for item in data if item["Position"] == 1)
        # test if we found the right entry for active_energy_tariff_2
        if not (
            active_energy_tariff_2["UnitStr"] == "Wh"
            and active_energy_tariff_2["DescriptionStr"] == "Energy"
        ):
            raise ValueError(
                "Did not find the required Fields for active_energy_tariff_2 in the JSON response from the "
                "M-Bus Center"
            )

        active_power_phase_1 = next(item for item in data if item["Position"] == 2)
        # test if we found the right entry for active_power_phase_1
        if not (
            active_power_phase_1["UnitStr"] == "W"
            and active_power_phase_1["DescriptionStr"] == "Power (vendor specific)"
        ):
            raise ValueError(
                "Did not find the required Fields for active_power_phase_1 in the JSON response from the "
                "M-Bus Center"
            )

        active_power_phase_2 = next(item for item in data if item["Position"] == 3)
        # test if we found the right entry for active_power_phase_2
        if not (
            active_power_phase_2["UnitStr"] == "W"
            and active_power_phase_2["DescriptionStr"] == "Power (vendor specific)"
        ):
            raise ValueError(
                "Did not find the required Fields for active_power_phase_2 in the JSON response from the "
                "M-Bus Center"
            )

        active_power_phase_3 = next(item for item in data if item["Position"] == 4)
        # test if we found the right entry for power_phase_3
        if not (
            active_power_phase_3["UnitStr"] == "W"
            and active_power_phase_3["DescriptionStr"] == "Power (vendor specific)"
        ):
            raise ValueError(
                "Did not find the required Fields for active_power_phase_3 in the JSON response from the "
                "M-Bus Center"
            )

        power_all_phases = next(item for item in data if item["Position"] == 5)
        # test if we found the right entry for power_phase_3
        if not (
            power_all_phases["UnitStr"] == "W"
            and power_all_phases["DescriptionStr"] == "Power"
        ):
            raise ValueError(
                "Did not find the required Fields for power_all_phases in the JSON response from the "
                "M-Bus Center"
            )

        voltage_phase_1 = next(item for item in data if item["Position"] == 6)
        # test if we found the right entry voltage_phase_1
        if not (
            voltage_phase_1["UnitStr"] == "V"
            and voltage_phase_1["DescriptionStr"] == "Volts (vendor specific)"
        ):
            raise ValueError(
                "Did not find the required Fields for voltage_phase_1 in the JSON response from the "
                "M-Bus Center"
            )

        voltage_phase_2 = next(item for item in data if item["Position"] == 7)
        # test if we found the right entry voltage_phase_2
        if not (
            voltage_phase_2["UnitStr"] == "V"
            and voltage_phase_2["DescriptionStr"] == "Volts (vendor specific)"
        ):
            raise ValueError(
                "Did not find the required Fields for voltage_phase_2 in the JSON response from the "
                "M-Bus Center"
            )

        voltage_phase_3 = next(item for item in data if item["Position"] == 8)
        # test if we found the right entry voltage_phase_3
        if not (
            voltage_phase_3["UnitStr"] == "V"
            and voltage_phase_3["DescriptionStr"] == "Volts (vendor specific)"
        ):
            raise ValueError(
                "Did not find the required Fields for voltage_phase_3 in the JSON response from the "
                "M-Bus Center"
            )

        current_phase_1 = next(item for item in data if item["Position"] == 9)
        # test if we found the right entry current_phase_1
        if not (
            current_phase_1["UnitStr"] == "A"
            and current_phase_1["DescriptionStr"] == "Ampere (vendor specific)"
        ):
            raise ValueError(
                "Did not find the required Fields for current_phase_1 in the JSON response from the "
                "M-Bus Center"
            )

        current_phase_2 = next(item for item in data if item["Position"] == 10)
        # test if we found the right entry current_phase_2
        if not (
            current_phase_2["UnitStr"] == "A"
            and current_phase_2["DescriptionStr"] == "Ampere (vendor specific)"
        ):
            raise ValueError(
                "Did not find the required Fields for current_phase_2 in the JSON response from the "
                "M-Bus Center"
            )

        current_phase_3 = next(item for item in data if item["Position"] == 11)
        # test if we found the right entry current_phase_3
        if not (
            current_phase_3["UnitStr"] == "A"
            and current_phase_3["DescriptionStr"] == "Ampere (vendor specific)"
        ):
            raise ValueError(
                "Did not find the required Fields for current_phase_3 in the JSON response from the "
                "M-Bus Center"
            )

        current_all_phases = next(item for item in data if item["Position"] == 12)
        # test if we found the right entry current_all_phases
        if not (
            current_all_phases["UnitStr"] == "A"
            and current_all_phases["DescriptionStr"] == "Ampere"
        ):
            raise ValueError(
                "Did not find the required Fields for current_all_phases in the JSON response from the "
                "M-Bus Center"
            )

        frequency = next(item for item in data if item["Position"] == 13)
        # test if we found the right entry frequency
        if not (
            (frequency["UnitStr"] == "None" or frequency["UnitStr"] == "Hz")
            and frequency["DescriptionStr"] == "Special supplier information"
        ):
            raise ValueError(
                "Did not find the required Fields for frequency in the JSON response from the "
                "M-Bus Center"
            )

        resets = next(item for item in data if item["Position"] == 14)
        # test if we found the right entry resets
        if not (
            resets["UnitStr"] == "None" and resets["DescriptionStr"] == "Reset counter"
        ):
            raise ValueError(
                "Did not find the required Fields for resets in the JSON response from the "
                "M-Bus Center"
            )

        current_transformer_factor = next(
            item for item in data if item["Position"] == 15
        )
        # test if we found the right entry current_transformer_factor
        if not (
            current_transformer_factor["UnitStr"] == "None"
            and current_transformer_factor["DescriptionStr"]
            == "Special supplier information"
        ):
            raise ValueError(
                "Did not find the required Fields for current_transformer_factor in the JSON response from the "
                "M-Bus Center"
            )

        error_flags = next(item for item in data if item["Position"] == 16)
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
            ACTIVE_ENERGY_TARIFF_1: int(active_energy_tariff_1["LoggerLastValue"])
            / 1000,
            ACTIVE_ENERGY_TARIFF_2: int(active_energy_tariff_2["LoggerLastValue"])
            / 1000,
            ACTIVE_POWER_PHASE_1: int(active_power_phase_1["LoggerLastValue"]) / 1000,
            ACTIVE_POWER_PHASE_2: int(active_power_phase_2["LoggerLastValue"]) / 1000,
            ACTIVE_POWER_PHASE_3: int(active_power_phase_3["LoggerLastValue"]) / 1000,
            ACTIVE_POWER_ALL_PHASES: int(power_all_phases["LoggerLastValue"]) / 1000,
            VOLTAGE_PHASE_1: int(voltage_phase_1["LoggerLastValue"]),
            VOLTAGE_PHASE_2: int(voltage_phase_2["LoggerLastValue"]),
            VOLTAGE_PHASE_3: int(voltage_phase_3["LoggerLastValue"]),
            CURRENT_PHASE_1: int(current_phase_1["LoggerLastValue"]),
            CURRENT_PHASE_2: int(current_phase_2["LoggerLastValue"]),
            CURRENT_PHASE_3: int(current_phase_3["LoggerLastValue"]),
            CURRENT_ALL_PHASES: int(current_all_phases["LoggerLastValue"]),
            FREQUENCY: int(frequency["LoggerLastValue"]) / 10,
            RESET_COUNTER: int(resets["LoggerLastValue"]),
            CURRENT_TRANSFORMER_FACTOR: int(
                current_transformer_factor["LoggerLastValue"]
            ),
            ERROR_FLAGS: int(error_flags["LoggerLastValue"]),
        }
