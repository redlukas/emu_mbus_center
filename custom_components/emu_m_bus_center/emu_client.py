"""Interact with the M-Bus Center over HTTP REST calls."""

import logging

import aiohttp

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

    def __init__(self, ip, update_coordinator: DataUpdateCoordinator | None = None):
        """Create a new EmuApiClient object."""
        self._ip = ip
        self._update_coordinator = update_coordinator

    async def validate_connection_async(
        self, sensors: list | None
    ) -> dict[str, bool | list]:
        """See if we have a good connection to the M-Bus Center asynchronously."""
        result = {
            "found_center": False,
            "found_all_sensors": False,
            "good_sensors": [],
            "bad_sensors": [],
        }

        async with aiohttp.ClientSession() as session:
            # Check if main page contains the logo
            try:
                async with session.get(
                    f"http://{self._ip}", timeout=10
                ) as main_page_response:
                    text = await main_page_response.text()
                    if "emu_logo_128px" in text:
                        result["found_center"] = True
            except aiohttp.ClientError as ce:
                _LOGGER.error(
                    "Validate Connection could not reach M-Bus Center on %s: %s",
                    self._ip,
                    ce,
                )
                return result

            if sensors is None or len(sensors) == 0:
                _LOGGER.debug("Sensors was None or length 0")
                return {**result, "found_all_sensors": True}

            # Sequentially validate each sensor
            for sensor in sensors:
                url = f"http://{self._ip}/app/api/id/{sensor.sensor_id}.json"
                try:
                    async with session.get(url, timeout=10) as api_response:
                        parsed = (await api_response.json()).get("Device")

                    # test if we got the Info for the right device
                    if parsed.get("Id") != int(sensor.sensor_id):
                        _LOGGER.warning(
                            "Got Info for the wrong Sensor! Expected %i, got %s",
                            sensor.sensor_id,
                            parsed.get("Id"),
                        )
                        result["bad_sensors"].append(sensor.sensor_id)
                        continue

                    # Validate supported measurement type
                    if parsed.get("Medium") not in get_supported_measurement_types():
                        _LOGGER.warning(
                            "Sensor %i does not provide a measurement type we know how to handle",
                            sensor.sensor_id,
                        )
                        result["bad_sensors"].append(sensor.sensor_id)
                        continue

                    result["good_sensors"].append(sensor.sensor_id)

                except aiohttp.ContentTypeError:
                    _LOGGER.warning(
                        "Center on %s did not return a valid JSON for Sensor %i",
                        self._ip,
                        sensor.sensor_id,
                    )
                    result["bad_sensors"].append(sensor.sensor_id)
                except (ValueError, KeyError, aiohttp.ClientError) as e:
                    _LOGGER.error(
                        "Unexpected error when parsing response for Sensor %i: %s",
                        sensor.sensor_id,
                        e,
                    )
                    result["bad_sensors"].append(sensor.sensor_id)

        return {
            **result,
            "found_all_sensors": len(result["good_sensors"]) == len(sensors),
        }

    async def scan_for_sensors_async(self) -> list[Generic_sensor]:
        """Scan for available sensors on the M-Bus Center asynchronously."""
        list_of_ids = []

        async with aiohttp.ClientSession() as session:
            for sensor_id in range(250):
                try:
                    url = f"http://{self._ip}/app/api/id/{sensor_id}.json"
                    async with session.get(url, timeout=10) as response:
                        if response.status != 200:
                            _LOGGER.debug(
                                "No Sensor on ID %s (status %d)",
                                sensor_id,
                                response.status,
                            )
                            continue

                        parsed = (await response.json()).get("Device")

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
                                    "No device template found for sensor id %i with serial %s. "
                                    "Reported Version is %i and sensor count is %i. "
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
                                        else parsed.get("Name") or parsed.get("Serial")
                                    ),
                                    device_type=device_type,
                                )
                            )
                            _LOGGER.debug("%s on ID %i", device_type, sensor_id)
                        else:
                            _LOGGER.error(
                                "Sensor %i did not supply a proper serial number",
                                sensor_id,
                            )

                except aiohttp.ClientConnectionError:
                    _LOGGER.debug("No Sensor on ID %s (connection error)", sensor_id)
                except aiohttp.ContentTypeError:
                    _LOGGER.error(
                        "Center on %s did not return valid JSON for Sensor %i",
                        self._ip,
                        sensor_id,
                    )
                except (ValueError, KeyError) as e:
                    _LOGGER.error(
                        "Response from M-Bus Center did not satisfy expectations: %s", e
                    )

        return list_of_ids

    async def read_sensor_async(self, sensor_id: int):
        """Fetch new state data for the sensor asynchronously."""
        if self._update_coordinator is None:
            raise ValueError(
                "update_coordinator must be set before calling read_sensor_async"
            )

        url = f"http://{self._ip}/app/api/id/{sensor_id}.json"

        def raise_error(message: str, exception_type: type[Exception]):
            _LOGGER.error(
                "%s during read_sensor_async: %s", exception_type.__name__, message
            )

        try:
            async with (
                aiohttp.ClientSession() as session,
                session.get(url, timeout=10) as response,
            ):
                if response.status != 200:
                    raise_error(
                        f"Unexpected status code: {response.status}", CannotConnect
                    )
                    return None

                parsed = (await response.json()).get("Device")

            if parsed.get("Id") != int(sensor_id):
                raise_error("wrong ID", ValueError)

            if parsed.get("Medium") not in get_supported_measurement_types():
                raise_error(
                    "The M-Bus Center sent a valid response, but the sensor does not provide Electricity measurements",
                    ValueError,
                )

            if self._update_coordinator.version_number != int(
                parsed.get("Version")
            ) and self._update_coordinator.sensor_count == len(
                parsed.get("ValueDescs")
            ):
                raise_error(
                    "The M-Bus Center sent a valid response, but the sensor does not match the device template",
                    EmuApiError,
                )
            return self._update_coordinator.parse(parsed.get("ValueDescs"))

        except aiohttp.ClientConnectionError as ce:
            msg = str(ce)
            if "Max retries exceeded" in msg:
                raise_error(
                    f"Could not reach M-Bus Center on {self._ip}", CannotConnect
                )
            elif "Remote end closed connection" in msg:
                raise_error(f"Could not find sensor with ID {sensor_id}", CannotConnect)
            else:
                raise_error(f"generic connection error: {ce}", CannotConnect)
        except aiohttp.ContentTypeError:
            raise_error(
                f"Center on {self._ip} did not return valid JSON for Sensor {sensor_id}",
                CannotConnect,
            )
        except (ValueError, KeyError) as e:
            raise_error(
                f"Response from M-Bus Center did not satisfy expectations: {e}",
                CannotConnect,
            )


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
