import json
import logging

import requests
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .device_types.devices import Device_type
from .device_types.devices import get_enum_from_version_and_sensor_count
from .device_types.devices import get_supported_measurement_types

_LOGGER = logging.getLogger(__name__)


class EmuApiClient:
    def __init__(self, ip, device: DataUpdateCoordinator | None = None):
        self._ip = ip
        self._device = device

    def validate_connection_sync(self, sensors: list | None):
        try:
            res = requests.get(f"http://{self._ip}")
            if "emu_logo_128px" not in res.text:
                return False

            if sensors is not None:
                found_valid_sensor = False
                for (
                    sensor_id,
                    serial,
                    given_name,
                    device_type,
                ) in sensors:
                    res = requests.get(f"http://{self._ip}/app/api/id/{sensor_id}.json")
                    try:
                        parsed = json.loads(res.text).get("Device")

                        # test if we got the Info for the right device
                        if not parsed.get("Id") == int(sensor_id):
                            _LOGGER.warning(
                                f"Got Info for the wrong Sensor! Expected {sensor_id}, got {parsed.get('Id')}"
                            )
                            continue
                        # test if the sensor we read out does in fact provide measurements we know how to handle
                        if (
                            not parsed.get("Medium")
                            in get_supported_measurement_types()
                        ):
                            _LOGGER.warning(
                                f"Sensor {sensor_id} does not provide a measurement type we know how to handle"
                            )
                            continue
                        # if we find no objections, we can go on and set the flag
                        found_valid_sensor = True
                    except json.decoder.JSONDecodeError:
                        _LOGGER.warning(
                            f"Center on {self._ip} did not return a valid JSON for Sensor {sensor_id}"
                        )
                        continue
                if not found_valid_sensor:
                    _LOGGER.error("Found no Sensors with valid return Format")
                    return False

            return True

        except requests.exceptions.ConnectionError as ce:
            if "Max retries exceeded" in ce.__str__():
                _LOGGER.error(f"Could not reach M-Bus Center on {self._ip}")
            raise CannotConnect
        except BaseException as e:
            _LOGGER.error(
                f"generic exception while validating connection to center {self._ip}: {e}"
            )
            return False

    async def validate_connection_async(
        self, hass: HomeAssistant, sensors: list | None
    ):
        return await hass.async_add_executor_job(self.validate_connection_sync, sensors)

    def scan_for_sensors_sync(self) -> list[(int, int, str, str, int, Device_type)]:
        list_of_ids = list()
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
                                f"No device template found for sensor id {sensor_id} with serial {parsed.get('Serial')}."
                                f"Reported Version is {int(parsed.get('Version'))} and sensor count is {len(parsed.get('ValueDescs'))}."
                                f"Manufacturer is {parsed.get('ManufacturerId')}, medium is {parsed.get('Medium')}"
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
                            f"Sensor {sensor_id} did not supply a proper serial number"
                        )
            except requests.exceptions.ConnectionError:
                _LOGGER.error(f"No Sensor on ID {sensor_id}")
            except json.decoder.JSONDecodeError:
                _LOGGER.error(
                    f"Center on {self._ip} did not return a valid JSON for Sensor {sensor_id}"
                )
            except (ValueError, KeyError) as e:
                _LOGGER.error(
                    "Response from M-Bus Center did not satisfy expectations:", e
                )
        return list_of_ids

    async def scan_for_sensors_async(self, hass: HomeAssistant):
        return await hass.async_add_executor_job(self.scan_for_sensors_sync)

    def read_sensor_sync(self, sensor_id: int) -> dict[str, float]:
        """Fetch new state data for the sensor."""
        if self._device is None:
            raise ValueError("device must be set before calling read_sensor_sync")

        try:
            res = requests.get(f"http://{self._ip}/app/api/id/{sensor_id}.json")
            parsed = json.loads(res.text).get("Device")

            # test if we got the Info for the right device
            if not parsed.get("Id") == int(sensor_id):
                _LOGGER.error("wrong ID")
                raise ValueError("Got Info for the wrong Sensor!")
            # test if the sensor we read out does in fact provide electricity measurements
            if not parsed.get("Medium") in get_supported_measurement_types():
                raise ValueError(
                    "The M-Bus Center sent a valid response, but the sensor does not provide Electricity "
                    "measurements"
                )

            if not self._device.version_number == int(
                parsed.get("Version")
            ) and self._device.sensor_count == len(parsed.get("ValueDescs")):
                _LOGGER.error("Wrong template")
                raise EmuApiError(
                    "The M-Bus Center sent a valid response, but the sensor does not match the device template"
                )
            return self._device.parse(parsed.get("ValueDescs"))

        except requests.exceptions.ConnectionError as ce:
            if "Max retries exceeded" in ce.__str__():
                _LOGGER.error(f"Could not reach M-Bus Center on {self._ip}")
            elif "Remote end closed connection without response" in ce.__str__():
                _LOGGER.error(
                    f"Could not find sensor with ID {sensor_id} on M-Bus Center {self._ip}"
                )
            else:
                _LOGGER.error("generic connection error", ce)
            raise CannotConnect
        except json.decoder.JSONDecodeError:
            _LOGGER.error(
                f"Center on {self._ip} did not return a valid JSON for Sensor {sensor_id}"
            )
        except (ValueError, KeyError) as e:
            _LOGGER.error("Response from M-Bus Center did not satisfy expectations:", e)

    async def read_sensor_async(self, sensor_id: int, hass: HomeAssistant):
        result = await hass.async_add_executor_job(self.read_sensor_sync, sensor_id)
        # _LOGGER.error(f"result in read_sensor_async is {result}")
        return result


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""


class EmuApiError(HomeAssistantError):
    """Generic API errors"""

    def __init__(self, sta: str, msg: str | None = None) -> None:
        """sta: status code, msg: message"""
        Exception.__init__(self)
        self.sta = sta
        self.msg = msg

    def __str__(self):
        return f"<Emu API Error sta:{self.sta} message:{self.msg}>"
