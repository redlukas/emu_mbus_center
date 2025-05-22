"""Interact with the M-Bus Center over HTTP REST calls."""
import json
import logging

import requests

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .device_types.devices import (
    Device_type,
    get_enum_from_version_and_sensor_count,
    get_supported_measurement_types,
)

_LOGGER = logging.getLogger(__name__)


class EmuApiClient:
    """Wrap the API of the M-Bus Center."""

    def __init__(self, ip, device: DataUpdateCoordinator | None = None):
        """Create a new EmuApiClient object."""
        self._ip = ip
        self._device = device

    def validate_connection_sync(self, sensors: list | None):
        """See if we have a good connection to the M-Bus Center."""
        try:
            res = requests.get(f"http://{self._ip}")
            if "emu_logo_128px" not in res.text:
                return False

            if sensors is not None:
                found_valid_sensor = False
                for (
                    sensor_id,
                    _,
                    _,
                    _,
                ) in sensors:
                    res = requests.get(f"http://{self._ip}/app/api/id/{sensor_id}.json")
                    try:
                        parsed = json.loads(res.text).get("Device")

                        # test if we got the Info for the right device
                        if parsed.get("Id") != int(sensor_id):
                            _LOGGER.warning(
                                "Got Info for the wrong Sensor! Expected %i, got %s", sensor_id, parsed.get('Id')
                            )
                            continue
                        # test if the sensor we read out does in fact provide measurements we know how to handle
                        if (
                            parsed.get("Medium") not in get_supported_measurement_types()
                        ):
                            _LOGGER.warning(
                                "Sensor %i does not provide a measurement type we know how to handle", sensor_id
                            )
                            continue
                        # if we find no objections, we can go on and set the flag
                        found_valid_sensor = True
                    except json.decoder.JSONDecodeError:
                        _LOGGER.warning(
                            "Center on %d did not return a valid JSON for Sensor %i", self._ip, sensor_id
                        )
                        continue
                if not found_valid_sensor:
                    _LOGGER.error("Found no Sensors with valid return Format")
                    return False

            return True

        except requests.exceptions.ConnectionError as ce:
            if "Max retries exceeded" in ce.__str__():
                _LOGGER.error("Could not reach M-Bus Center on %s", self._ip)
            raise CannotConnect from ce

    async def validate_connection_async(
        self, hass: HomeAssistant, sensors: list | None
    ):
        """Enqueue the sync call in Home Assistant's executor."""
        return await hass.async_add_executor_job(self.validate_connection_sync, sensors)

    def scan_for_sensors_sync(self) -> list[(int, int, str, str, int, Device_type)]:
        """Scan for available sensors on the M-Bus Center."""
        list_of_ids = []
        for sensor_id in range(250):
            try:
                res = requests.get(f"http://{self._ip}/app/api/id/{sensor_id}.json")
                parsed = json.loads(res.text).get("Device")
                if parsed.get("Medium") in get_supported_measurement_types():
                    if (
                        parsed.get("Serial")
                        and int(parsed.get("Serial"))
                        and parsed.get("Version")
                        and int(parsed.get("Version"))
                        and parsed.get("ValueDescs")
                        and len(parsed.get("ValueDescs")) > 0
                    ):
                        device_type = get_enum_from_version_and_sensor_count(
                            version=int(parsed.get("Version")),
                            sensor_count=len(parsed.get("ValueDescs")),
                        )
                        if device_type is None:
                            _LOGGER.warning(
                                "No device template found for sensor id %i with serial %s."
                                "Reported Version is %i and sensor count is %i."
                                "Manufacturer is %s, medium is %s", sensor_id, parsed.get('Serial'), int(parsed.get('Version')), len(parsed.get('ValueDescs')), parsed.get('ManufacturerId'), parsed.get('Medium')
                            )
                        list_of_ids.append(
                            (
                                int(sensor_id),
                                int(parsed.get("Serial")),
                                (
                                    f"{parsed.get('Name')} ({parsed.get('Site')})"
                                    if parsed.get("Site") and parsed.get("Name")
                                    else (
                                        parsed.get("Name")
                                        if parsed.get("Name")
                                        else parsed.get("Serial")
                                    )
                                ),
                                device_type,
                            )
                        )
                    else:
                        _LOGGER.error(
                            "Sensor %i did not supply a proper serial number", sensor_id
                        )
            except requests.exceptions.ConnectionError:
                _LOGGER.error("No Sensor on ID %s", sensor_id)
            except json.decoder.JSONDecodeError:
                _LOGGER.error(
                    "Center on %s did not return a valid JSON for Sensor %i", self._ip, sensor_id
                )
            except (ValueError, KeyError) as e:
                _LOGGER.error(
                    "Response from M-Bus Center did not satisfy expectations: %s", e
                )
        return list_of_ids

    async def scan_for_sensors_async(self, hass: HomeAssistant):
        """Enqueue the sync call in Home Assistant's executor."""
        return await hass.async_add_executor_job(self.scan_for_sensors_sync)

    def read_sensor_sync(self, sensor_id: int) -> dict[str, float]:
        """Fetch new state data for the sensor."""
        if self._device is None:
            raise ValueError("device must be set before calling read_sensor_sync")

        try:
            res = requests.get(f"http://{self._ip}/app/api/id/{sensor_id}.json")
            parsed = json.loads(res.text).get("Device")

            # test if we got the Info for the right device
            if parsed.get("Id") != int(sensor_id):
                _LOGGER.error("wrong ID")
                raise ValueError("Got Info for the wrong Sensor!")
            # test if the sensor we read out does in fact provide electricity measurements
            if parsed.get("Medium") not in get_supported_measurement_types():
                raise ValueError(
                    "The M-Bus Center sent a valid response, but the sensor does not provide Electricity "
                    "measurements"
                )

            if self._device.version_number != int(parsed.get("Version")) and self._device.sensor_count == len(parsed.get("ValueDescs")):
                _LOGGER.error("Wrong template")
                raise EmuApiError(
                    "The M-Bus Center sent a valid response, but the sensor does not match the device template"
                )
            return self._device.parse(parsed.get("ValueDescs"))

        except requests.exceptions.ConnectionError as ce:
            if "Max retries exceeded" in ce.__str__():
                _LOGGER.error("Could not reach M-Bus Center on %s", self._ip)
            elif "Remote end closed connection without response" in ce.__str__():
                _LOGGER.error(
                    "Could not find sensor with ID %i on M-Bus Center %s", sensor_id, self._ip
                )
            else:
                _LOGGER.error("generic connection error: %s", ce)
            raise CannotConnect from ce
        except json.decoder.JSONDecodeError:
            _LOGGER.error(
                "Center on %s did not return a valid JSON for Sensor %i", self._ip, sensor_id
            )
        except (ValueError, KeyError) as e:
            _LOGGER.error("Response from M-Bus Center did not satisfy expectations: %s", e)

    async def read_sensor_async(self, sensor_id: int, hass: HomeAssistant):
        """Enqueue the sync call in Home Assistant's executor."""
        return await hass.async_add_executor_job(self.read_sensor_sync, sensor_id)


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""


class EmuApiError(HomeAssistantError):
    """Generic API errors."""

    def __init__(self, sta: str, msg: str | None = None) -> None:
        """sta: status code, msg: message."""
        Exception.__init__(self)
        self.sta = sta
        self.msg = msg

    def __str__(self):
        """Return a ustom string representation."""
        return f"<Emu API Error sta:{self.sta} message:{self.msg}>"
