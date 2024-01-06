import json
import logging

import requests
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .device_types.devices import Device_type
from .device_types.devices import get_enum_from_version_and_sensor_count

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
                for (
                    sensor_id,
                    serial,
                    given_name,
                    device_type,
                ) in sensors:
                    res = requests.get(f"http://{self._ip}/app/api/id/{sensor_id}.json")
                    try:
                        parsed = json.loads(res.text)["Device"]

                        # test if we got the Info for the right device
                        if not parsed["Id"] == int(sensor_id):
                            _LOGGER.error(
                                f"Got Info for the wrong Sensor! Expected {sensor_id}, got {parsed['Id']}"
                            )
                            return False
                        # test if the sensor we read out does in fact provide electricity measurements
                        if not parsed["Medium"] == "Electricity":
                            _LOGGER.error(
                                f"Sensor {sensor_id} does not provide electricity measurements"
                            )
                            return False
                    except json.decoder.JSONDecodeError:
                        _LOGGER.error(
                            f"Center on {self._ip} did not return a valid JSON for Sensor {sensor_id}"
                        )
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
                parsed = json.loads(res.text)["Device"]
                if parsed["Medium"] == "Electricity":
                    if (
                        parsed["Serial"]
                        and int(parsed["Serial"])
                        and parsed["Version"]
                        and int(parsed["Version"])
                        and parsed["ValueDescs"]
                        and len(parsed["ValueDescs"]) > 0
                    ):
                        device_type = get_enum_from_version_and_sensor_count(
                            version=int(parsed["Version"]),
                            sensor_count=len(parsed["ValueDescs"]),
                        )
                        if device_type is None:
                            raise EmuApiError(
                                f"No device template found for sensor id {sensor_id} with serial {parsed['Serial']}"
                            )
                        list_of_ids.append(
                            (
                                int(sensor_id),
                                int(parsed["Serial"]),
                                f"{parsed['Name']} ({parsed['Site']})"
                                if parsed["Site"] and parsed["Name"]
                                else parsed["Name"]
                                if parsed["Name"]
                                else parsed["Serial"],
                                device_type,
                            )
                        )
                    else:
                        _LOGGER.error(
                            f"Sensor {sensor_id} did not supply a proper serial number"
                        )
            except requests.exceptions.ConnectionError:
                _LOGGER.debug(f"No Sensor on ID {sensor_id}")
            except json.decoder.JSONDecodeError:
                _LOGGER.debug(
                    f"Center on {self._ip} did not return a valid JSON for Sensor {sensor_id}"
                )
            except (ValueError, KeyError) as e:
                _LOGGER.debug(
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
            parsed = json.loads(res.text)["Device"]

            # test if we got the Info for the right device
            if not parsed["Id"] == int(sensor_id):
                raise ValueError("Got Info for the wrong Sensor!")
            # test if the sensor we read out does in fact provide electricity measurements
            if not parsed["Medium"] == "Electricity":
                raise ValueError(
                    "The M-Bus Center sent a valid response, but the sensor does not provide Electricity "
                    "measurements"
                )

            if not self._device.version_number == int(
                parsed["Version"]
            ) and self._device.sensor_count == len(parsed["ValueDescs"]):
                raise EmuApiError(
                    "The M-Bus Center sent a valid response, but the sensor does not match the device template"
                )
            return self._device.parse(parsed["ValueDescs"])

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
