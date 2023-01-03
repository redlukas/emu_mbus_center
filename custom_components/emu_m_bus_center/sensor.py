"""Platform for sensor integration."""
from __future__ import annotations

import json
import logging
from datetime import timedelta

import homeassistant.helpers.config_validation as cv
import requests
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor import SensorStateClass
from homeassistant.const import CONF_IP_ADDRESS
from homeassistant.const import CONF_UNIQUE_ID
from homeassistant.const import UnitOfEnergy
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.typing import DiscoveryInfoType

_LOGGER = logging.getLogger("Emu Yaml Sensor")
SCAN_INTERVAL = timedelta(seconds=60)

# Validation of the user's config
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_IP_ADDRESS): cv.string,
        vol.Required(CONF_UNIQUE_ID): cv.ensure_list,
    }
)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""
    for entry in config[CONF_UNIQUE_ID]:
        item = entry.popitem(True)
        sensor = {"name": item[0], "ip_address": config[CONF_IP_ADDRESS], "id": item[1]}
        add_entities([EmuMBusCenterSensor(sensor)], True)
        """The "true" argument assures the values get fetched before the first write to HA"""


class EmuMBusCenterSensor(SensorEntity):
    """emu_m_bus_center Sensor class."""

    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_has_entity_name: True
    _attr_icon = "mdi:lightning-bolt"
    _attr_should_poll: True

    def __init__(self, sensor) -> None:
        self._name = sensor["name"]
        self._ip = sensor["ip_address"]
        self._id = sensor["id"]

    @property
    def name(self) -> str:
        """Return the display name of this sensor."""
        return self._name

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        try:
            res = requests.get(f"http://{self._ip}/app/api/id/{self._id}.json")
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

            energy_tarif_1 = next(item for item in parsed if item["Position"] == 0)
            # test if we found the right entry for energy_tarif_1
            if not (
                energy_tarif_1["UnitStr"] == "Wh"
                and energy_tarif_1["DescriptionStr"] == "Energy"
            ):
                raise ValueError(
                    "Did not find the required Fields for energy_tarif_1 in the JSON response from the "
                    "M-Bus Center"
                )

            energy_tarif_2 = next(item for item in parsed if item["Position"] == 1)
            # test if we found the right entry for energy_tarif_2
            if not (
                energy_tarif_2["UnitStr"] == "Wh"
                and energy_tarif_2["DescriptionStr"] == "Energy"
            ):
                raise ValueError(
                    "Did not find the required Fields for energy_tarif_2 in the JSON response from the "
                    "M-Bus Center"
                )

            power_phase_1 = next(item for item in parsed if item["Position"] == 2)
            # test if we found the right entry for power_phase_1
            if not (
                power_phase_1["UnitStr"] == "W"
                and power_phase_1["DescriptionStr"] == "Power (vendor specific)"
            ):
                raise ValueError(
                    "Did not find the required Fields for power_phase_1 in the JSON response from the "
                    "M-Bus Center"
                )

            power_phase_2 = next(item for item in parsed if item["Position"] == 3)
            # test if we found the right entry for power_phase_2
            if not (
                power_phase_2["UnitStr"] == "W"
                and power_phase_2["DescriptionStr"] == "Power (vendor specific)"
            ):
                raise ValueError(
                    "Did not find the required Fields for power_phase_2 in the JSON response from the "
                    "M-Bus Center"
                )

            power_phase_3 = next(item for item in parsed if item["Position"] == 4)
            # test if we found the right entry for power_phase_3
            if not (
                power_phase_3["UnitStr"] == "W"
                and power_phase_3["DescriptionStr"] == "Power (vendor specific)"
            ):
                raise ValueError(
                    "Did not find the required Fields for power_phase_3 in the JSON response from the "
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

            volts_phase_1 = next(item for item in parsed if item["Position"] == 6)
            # test if we found the right entry volts_phase_1
            if not (
                volts_phase_1["UnitStr"] == "V"
                and volts_phase_1["DescriptionStr"] == "Volts (vendor specific)"
            ):
                raise ValueError(
                    "Did not find the required Fields for volts_phase_1 in the JSON response from the "
                    "M-Bus Center"
                )

            volts_phase_2 = next(item for item in parsed if item["Position"] == 7)
            # test if we found the right entry volts_phase_2
            if not (
                volts_phase_2["UnitStr"] == "V"
                and volts_phase_2["DescriptionStr"] == "Volts (vendor specific)"
            ):
                raise ValueError(
                    "Did not find the required Fields for volts_phase_2 in the JSON response from the "
                    "M-Bus Center"
                )

            volts_phase_3 = next(item for item in parsed if item["Position"] == 8)
            # test if we found the right entry volts_phase_3
            if not (
                volts_phase_3["UnitStr"] == "V"
                and volts_phase_3["DescriptionStr"] == "Volts (vendor specific)"
            ):
                raise ValueError(
                    "Did not find the required Fields for volts_phase_3 in the JSON response from the "
                    "M-Bus Center"
                )

            ampere_phase_1 = next(item for item in parsed if item["Position"] == 9)
            # test if we found the right entry ampere_phase_1
            if not (
                ampere_phase_1["UnitStr"] == "A"
                and ampere_phase_1["DescriptionStr"] == "Ampere (vendor specific)"
            ):
                raise ValueError(
                    "Did not find the required Fields for ampere_phase_1 in the JSON response from the "
                    "M-Bus Center"
                )

            ampere_phase_2 = next(item for item in parsed if item["Position"] == 10)
            # test if we found the right entry ampere_phase_2
            if not (
                ampere_phase_2["UnitStr"] == "A"
                and ampere_phase_2["DescriptionStr"] == "Ampere (vendor specific)"
            ):
                raise ValueError(
                    "Did not find the required Fields for ampere_phase_2 in the JSON response from the "
                    "M-Bus Center"
                )

            ampere_phase_3 = next(item for item in parsed if item["Position"] == 11)
            # test if we found the right entry ampere_phase_3
            if not (
                ampere_phase_3["UnitStr"] == "A"
                and ampere_phase_3["DescriptionStr"] == "Ampere (vendor specific)"
            ):
                raise ValueError(
                    "Did not find the required Fields for ampere_phase_3 in the JSON response from the "
                    "M-Bus Center"
                )

            ampere_all_phases = next(item for item in parsed if item["Position"] == 12)
            # test if we found the right entry ampere_all_phases
            if not (
                ampere_all_phases["UnitStr"] == "A"
                and ampere_all_phases["DescriptionStr"] == "Ampere"
            ):
                raise ValueError(
                    "Did not find the required Fields for ampere_all_phases in the JSON response from the "
                    "M-Bus Center"
                )

            self._attr_native_value = energy_tarif_1["LoggerLastValue"] / 1000
            self._attr_extra_state_attributes = {
                "energy_tarif_2": energy_tarif_2["LoggerLastValue"] / 1000,
                "power_phase_1": power_phase_1["LoggerLastValue"] / 1000,
                "power_phase_2": power_phase_2["LoggerLastValue"] / 1000,
                "power_phase_3": power_phase_3["LoggerLastValue"] / 1000,
                "power_all_phases": power_all_phases["LoggerLastValue"] / 1000,
                "volts_phase_1": volts_phase_1["LoggerLastValue"],
                "volts_phase_2": volts_phase_2["LoggerLastValue"],
                "volts_phase_3": volts_phase_3["LoggerLastValue"],
                "ampere_phase_1": ampere_phase_1["LoggerLastValue"],
                "ampere_phase_2": ampere_phase_2["LoggerLastValue"],
                "ampere_phase_3": ampere_phase_3["LoggerLastValue"],
                "ampere_all_phases": ampere_all_phases["LoggerLastValue"],
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
