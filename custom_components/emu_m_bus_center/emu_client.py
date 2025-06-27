"""Interact with the M-Bus Center over HTTP REST calls."""

import json
import logging

import requests

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .device_types.devices import (
    Generic_sensor,
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

    def validate_connection_sync(self, sensors: list | None) -> dict[str, bool | list]:
        """See if we have a good connection to the M-Bus Center."""
        result = {
            "found_center": False,
            "found_all_sensors": False,
            "good_sensors": [],
            "bad_sensors": [],
        }
        try:
            main_page_response = requests.get(f"http://{self._ip}")
            if "emu_logo_128px" in main_page_response.text:
                result["found_center"] = True

            if sensors is None or len(sensors) == 0:
                _LOGGER.debug("Sensors was none or len 0")
                return {**result, "found_all_sensors": True}
            for sensor in sensors:
                api_response = requests.get(
                    f"http://{self._ip}/app/api/id/{sensor.sensor_id}.json"
                )
                try:
                    parsed = json.loads(api_response.text).get("Device")

                    # test if we got the Info for the right device
                    if parsed.get("Id") != int(sensor.sensor_id):
                        _LOGGER.warning(
                            "Got Info for the wrong Sensor! Expected %i, got %s",
                            sensor.sensor_id,
                            parsed.get("Id"),
                        )
                        result["bad_sensors"].append(sensor.sensor_id)
                        continue
                    # test if the sensor we read out does in fact provide measurements we know how to handle
                    if parsed.get("Medium") not in get_supported_measurement_types():
                        _LOGGER.warning(
                            "Sensor %i does not provide a measurement type we know how to handle",
                            sensor.sensor_id,
                        )
                        result["bad_sensors"].append(sensor.sensor_id)
                        continue
                    # if we find no objections, we can go on and set the flag
                    result["good_sensors"].append(sensor.sensor_id)
                except json.decoder.JSONDecodeError:
                    _LOGGER.warning(
                        "Center on %d did not return a valid JSON for Sensor %i",
                        self._ip,
                        sensor.sensor_id,
                    )
                    result["bad_sensors"].append(sensor.sensor_id)
                    continue

        except requests.exceptions.ConnectionError as ce:
            if "Max retries exceeded" in ce.__str__():
                _LOGGER.error(
                    "Validate Connection could not reach M-Bus Center on %s", self._ip
                )
            return result

        return {
            **result,
            "found_all_sensors": len(result["good_sensors"]) == len(sensors),
        }

    async def validate_connection_async(
        self, hass: HomeAssistant, sensors: list | None
    ) -> dict[str, bool | list]:
        """Enqueue the sync call in Home Assistant's executor."""
        return await hass.async_add_executor_job(self.validate_connection_sync, sensors)

    def scan_for_sensors_sync(self) -> list[Generic_sensor]:
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
                                "Manufacturer is %s, medium is %s",
                                sensor_id,
                                parsed.get("Serial"),
                                int(parsed.get("Version")),
                                len(parsed.get("ValueDescs")),
                                parsed.get("ManufacturerId"),
                                parsed.get("Medium"),
                            )
                        list_of_ids.append(
                            Generic_sensor(
                                sensor_id=int(sensor_id),
                                serial_number=int(parsed.get("Serial")),
                                name=(
                                    f"{parsed.get('Name')} ({parsed.get('Site')})"
                                    if parsed.get("Site") and parsed.get("Name")
                                    else (
                                        parsed.get("Name")
                                        if parsed.get("Name")
                                        else parsed.get("Serial")
                                    )
                                ),
                                device_type=device_type,
                            )
                        )
                    else:
                        _LOGGER.error(
                            "Sensor %i did not supply a proper serial number", sensor_id
                        )
            # ruff: noqa: PERF203
            except requests.exceptions.ConnectionError:
                _LOGGER.debug("No Sensor on ID %s", sensor_id)
            except json.decoder.JSONDecodeError:
                _LOGGER.error(
                    "Center on %s did not return a valid JSON for Sensor %i",
                    self._ip,
                    sensor_id,
                )
            except (ValueError, KeyError) as e:
                _LOGGER.error(
                    "Response from M-Bus Center did not satisfy expectations: %s", e
                )
        return list_of_ids

    async def scan_for_sensors_async(self, hass: HomeAssistant) -> list[Generic_sensor]:
        """Enqueue the sync call in Home Assistant's executor."""
        return await hass.async_add_executor_job(self.scan_for_sensors_sync)

    def read_sensor_sync(self, sensor_id: int) -> dict[str, float]:
        """Fetch new state data for the sensor."""
        if self._device is None:
            raise ValueError("device must be set before calling read_sensor_sync")

        def raise_error(message: str, exception_type: type[Exception]):
            _LOGGER.error(message)
            # raise exception_type(message)

        try:
            res = requests.get(f"http://{self._ip}/app/api/id/{sensor_id}.json")
            parsed = json.loads(res.text).get("Device")

            # test if we got the Info for the right device
            if parsed.get("Id") != int(sensor_id):
                raise_error("wrong ID", ValueError)
            # test if the sensor we read out does in fact provide electricity measurements
            if parsed.get("Medium") not in get_supported_measurement_types():
                raise_error(
                    "The M-Bus Center sent a valid response, but the sensor does not provide Electricity measurements",
                    ValueError,
                )

            if self._device.version_number != int(
                parsed.get("Version")
            ) and self._device.sensor_count == len(parsed.get("ValueDescs")):
                raise_error(
                    "The M-Bus Center sent a valid response, but the sensor does not match the device template",
                    EmuApiError,
                )
            return self._device.parse(parsed.get("ValueDescs"))

        except requests.exceptions.ConnectionError as ce:
            if "Max retries exceeded" in ce.__str__():
                raise_error(
                    f"Could not reach M-Bus Center on {self._ip}", CannotConnect
                )
            elif "Remote end closed connection without response" in ce.__str__():
                raise_error(
                    f"Could not find sensor with ID {sensor_id} on M-Bus Center {self._ip}",
                    CannotConnect,
                )
            else:
                raise_error(f"generic connection error: {ce}", CannotConnect)
        except json.decoder.JSONDecodeError:
            raise_error(
                f"Center on {self._ip} did not return a valid JSON for Sensor {sensor_id}",
                CannotConnect,
            )
        except (ValueError, KeyError) as e:
            raise_error(
                f"Response from M-Bus Center did not satisfy expectations: {e}",
                CannotConnect,
            )

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
