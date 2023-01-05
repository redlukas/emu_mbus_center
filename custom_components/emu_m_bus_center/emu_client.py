import json
import logging
import requests
from homeassistant.core import HomeAssistant
from .const import (ACTIVE_ENERGY_TARIFF_1, ACTIVE_ENERGY_TARIFF_2,
                    ACTIVE_POWER_PHASE_1, ACTIVE_POWER_PHASE_2, ACTIVE_POWER_PHASE_3, ACTIVE_POWER_ALL_PHASES,
                    VOLTAGE_PHASE_1, VOLTAGE_PHASE_2, VOLTAGE_PHASE_3,
                    CURRENT_PHASE_1, CURRENT_PHASE_2, CURRENT_PHASE_3, CURRENT_ALL_PHASES,
                    FREQUENCY, RESET_COUNTER, CURRENT_TRANSFORMER_FACTOR, ERROR_FLAGS)

_LOGGER = logging.getLogger(__name__)


class EmuApiError(Exception):
    """Generic API errors"""

    def __init__(self, sta: str, msg: str | None = None) -> None:
        """sta: status code, msg: message"""
        Exception.__init__(self)
        self.sta = sta
        self.msg = msg

    def __str__(self):
        return f"<Emu API Error sta:{self.sta} message:{self.msg}>"


class EmuApiClient:
    def __init__(self, ip):
        self._ip = ip

    def validate_connection_sync(self):
        try:
            res = requests.get(f"http://{self._ip}")
            _LOGGER.error(f"res is {res}")
            return True if "emu_logo_128px" in res.text else False
        except requests.exceptions.ConnectionError as ce:
            if "Max retries exceeded" in ce.__str__():
                _LOGGER.error(f"Could not reach M-Bus Center on {self._ip}")

            return False
        except BaseException as e:
            _LOGGER.error(f"generic exception while validation connection to center {self._ip}: {e}")
            return False

    async def validate_connection_async(self, hass: HomeAssistant):
        result = await hass.async_add_executor_job(self.validate_connection_sync)
        _LOGGER.error(f"awaited res is {result}")
        return result

    def read_sensor_sync(self, sensor_id: int):
        """Fetch new state data for the sensor."""
        try:
            res = requests.get(f"http://{self._ip}/app/api/id/{sensor_id}.json")
            parsed = json.loads(res.text)["Device"]

            # test if we got the Info for the right device
            if not parsed["Id"] == int(self._id):
                raise ValueError("Got Info for the wrong Sensor!")
            # test if the sensor we read out does in fact provide electricity measurements
            if not parsed["Medium"] == "Electricity":
                raise ValueError(
                    "The M-Bus Center sent a valid response, but the sensor does not provide Electricity "
                    "measurements"
                )

            parsed = parsed["ValueDescs"]

            active_energy_tariff_1 = next(item for item in parsed if item["Position"] == 0)
            # test if we found the right entry for active_energy_tariff_1
            if not (
                    active_energy_tariff_1["UnitStr"] == "Wh"
                    and active_energy_tariff_1["DescriptionStr"] == "Energy"
            ):
                raise ValueError(
                    "Did not find the required Fields for active_energy_tariff_1 in the JSON response from the "
                    "M-Bus Center"
                )

            active_energy_tariff_2 = next(item for item in parsed if item["Position"] == 1)
            # test if we found the right entry for active_energy_tariff_2
            if not (
                    active_energy_tariff_2["UnitStr"] == "Wh"
                    and active_energy_tariff_2["DescriptionStr"] == "Energy"
            ):
                raise ValueError(
                    "Did not find the required Fields for active_energy_tariff_2 in the JSON response from the "
                    "M-Bus Center"
                )

            active_power_phase_1 = next(item for item in parsed if item["Position"] == 2)
            # test if we found the right entry for active_power_phase_1
            if not (
                    active_power_phase_1["UnitStr"] == "W"
                    and active_power_phase_1["DescriptionStr"] == "Power (vendor specific)"
            ):
                raise ValueError(
                    "Did not find the required Fields for active_power_phase_1 in the JSON response from the "
                    "M-Bus Center"
                )

            active_power_phase_2 = next(item for item in parsed if item["Position"] == 3)
            # test if we found the right entry for active_power_phase_2
            if not (
                    active_power_phase_2["UnitStr"] == "W"
                    and active_power_phase_2["DescriptionStr"] == "Power (vendor specific)"
            ):
                raise ValueError(
                    "Did not find the required Fields for active_power_phase_2 in the JSON response from the "
                    "M-Bus Center"
                )

            active_power_phase_3 = next(item for item in parsed if item["Position"] == 4)
            # test if we found the right entry for power_phase_3
            if not (
                    active_power_phase_3["UnitStr"] == "W"
                    and active_power_phase_3["DescriptionStr"] == "Power (vendor specific)"
            ):
                raise ValueError(
                    "Did not find the required Fields for active_power_phase_3 in the JSON response from the "
                    "M-Bus Center"
                )

            power_all_phases = next(item for item in parsed if item["Position"] == 5)
            # test if we found the right entry for power_phase_3
            if not (
                    power_all_phases["UnitStr"] == "W"
                    and power_all_phases["DescriptionStr"] == "Power"
            ):
                raise ValueError(
                    "Did not find the required Fields for power_all_phases in the JSON response from the "
                    "M-Bus Center"
                )

            voltage_phase_1 = next(item for item in parsed if item["Position"] == 6)
            # test if we found the right entry voltage_phase_1
            if not (
                    voltage_phase_1["UnitStr"] == "V"
                    and voltage_phase_1["DescriptionStr"] == "Volts (vendor specific)"
            ):
                raise ValueError(
                    "Did not find the required Fields for voltage_phase_1 in the JSON response from the "
                    "M-Bus Center"
                )

            voltage_phase_2 = next(item for item in parsed if item["Position"] == 7)
            # test if we found the right entry voltage_phase_2
            if not (
                    voltage_phase_2["UnitStr"] == "V"
                    and voltage_phase_2["DescriptionStr"] == "Volts (vendor specific)"
            ):
                raise ValueError(
                    "Did not find the required Fields for voltage_phase_2 in the JSON response from the "
                    "M-Bus Center"
                )

            voltage_phase_3 = next(item for item in parsed if item["Position"] == 8)
            # test if we found the right entry voltage_phase_3
            if not (
                    voltage_phase_3["UnitStr"] == "V"
                    and voltage_phase_3["DescriptionStr"] == "Volts (vendor specific)"
            ):
                raise ValueError(
                    "Did not find the required Fields for voltage_phase_3 in the JSON response from the "
                    "M-Bus Center"
                )

            current_phase_1 = next(item for item in parsed if item["Position"] == 9)
            # test if we found the right entry current_phase_1
            if not (
                    current_phase_1["UnitStr"] == "A"
                    and current_phase_1["DescriptionStr"] == "Ampere (vendor specific)"
            ):
                raise ValueError(
                    "Did not find the required Fields for current_phase_1 in the JSON response from the "
                    "M-Bus Center"
                )

            current_phase_2 = next(item for item in parsed if item["Position"] == 10)
            # test if we found the right entry current_phase_2
            if not (
                    current_phase_2["UnitStr"] == "A"
                    and current_phase_2["DescriptionStr"] == "Ampere (vendor specific)"
            ):
                raise ValueError(
                    "Did not find the required Fields for current_phase_2 in the JSON response from the "
                    "M-Bus Center"
                )

            current_phase_3 = next(item for item in parsed if item["Position"] == 11)
            # test if we found the right entry current_phase_3
            if not (
                    current_phase_3["UnitStr"] == "A"
                    and current_phase_3["DescriptionStr"] == "Ampere (vendor specific)"
            ):
                raise ValueError(
                    "Did not find the required Fields for current_phase_3 in the JSON response from the "
                    "M-Bus Center"
                )

            current_all_phases = next(item for item in parsed if item["Position"] == 12)
            # test if we found the right entry current_all_phases
            if not (
                    current_all_phases["UnitStr"] == "A"
                    and current_all_phases["DescriptionStr"] == "Ampere"
            ):
                raise ValueError(
                    "Did not find the required Fields for current_all_phases in the JSON response from the "
                    "M-Bus Center"
                )

            frequency = next(item for item in parsed if item["Position"] == 13)
            # test if we found the right entry frequency
            if not (
                    (frequency["UnitStr"] == "None" or frequency["UnitStr"] == "Hz")
                    and frequency["DescriptionStr"] == "Special supplier information"
            ):
                raise ValueError(
                    "Did not find the required Fields for frequency in the JSON response from the "
                    "M-Bus Center"
                )

            resets = next(item for item in parsed if item["Position"] == 14)
            # test if we found the right entry resets
            if not (
                    resets["UnitStr"] == "None"
                    and resets["DescriptionStr"] == "Reset counter"
            ):
                raise ValueError(
                    "Did not find the required Fields for resets in the JSON response from the "
                    "M-Bus Center"
                )

            current_transformer_factor = next(item for item in parsed if item["Position"] == 15)
            # test if we found the right entry current_transformer_factor
            if not (
                    current_transformer_factor["UnitStr"] == "None"
                    and current_transformer_factor["DescriptionStr"] == "Special supplier information"
            ):
                raise ValueError(
                    "Did not find the required Fields for current_transformer_factor in the JSON response from the "
                    "M-Bus Center"
                )

            error_flags = next(item for item in parsed if item["Position"] == 16)
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
                ACTIVE_ENERGY_TARIFF_1: active_energy_tariff_1["LoggerLastValue"] / 1000,
                ACTIVE_ENERGY_TARIFF_2: active_energy_tariff_2["LoggerLastValue"] / 1000,
                ACTIVE_POWER_PHASE_1: active_power_phase_1["LoggerLastValue"] / 1000,
                ACTIVE_POWER_PHASE_2: active_power_phase_2["LoggerLastValue"] / 1000,
                ACTIVE_POWER_PHASE_3: active_power_phase_3["LoggerLastValue"] / 1000,
                ACTIVE_POWER_ALL_PHASES: power_all_phases["LoggerLastValue"] / 1000,
                VOLTAGE_PHASE_1: voltage_phase_1["LoggerLastValue"],
                VOLTAGE_PHASE_2: voltage_phase_2["LoggerLastValue"],
                VOLTAGE_PHASE_3: voltage_phase_3["LoggerLastValue"],
                CURRENT_PHASE_1: current_phase_1["LoggerLastValue"],
                CURRENT_PHASE_2: current_phase_2["LoggerLastValue"],
                CURRENT_PHASE_3: current_phase_3["LoggerLastValue"],
                CURRENT_ALL_PHASES: current_all_phases["LoggerLastValue"],
                FREQUENCY: frequency["LoggerLastValue"] / 10,
                RESET_COUNTER: resets["LoggerLastValue"],
                CURRENT_TRANSFORMER_FACTOR: current_transformer_factor["LoggerLastValue"],
                ERROR_FLAGS: error_flags["LoggerLastValue"]

            }
        except requests.exceptions.ConnectionError as ce:
            if "Max retries exceeded" in ce.__str__():
                _LOGGER.error(f"Could not reach M-Bus Center on {self._ip}")
            elif "Remote end closed connection without response" in ce.__str__():
                _LOGGER.error(
                    f"Could not find sensor with ID {self._id} on M-Bus Center {self._ip}"
                )
            else:
                _LOGGER.error("generic connection error", ce)
        except json.decoder.JSONDecodeError:
            _LOGGER.error(
                f"Center on {self._ip} did not return a valid JSON for Sensor {self._id}"
            )
        except (ValueError, KeyError) as e:
            _LOGGER.error("Response from M-Bus Center did not satisfy expectations:", e)

    async def read_sensor_async(self, sensor_id: int, hass: HomeAssistant):
        result = await hass.async_add_executor_job(self.read_sensor_sync(sensor_id))
        return result
