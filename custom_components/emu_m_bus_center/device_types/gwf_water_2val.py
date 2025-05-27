"""Sensor implementation for a 2 Value Water sensor."""
import inspect
import logging

from custom_components.emu_m_bus_center.const import SERIAL_NO, VOLUME
from custom_components.emu_m_bus_center.sensor import (
    EmuCoordinator,
    EmuSerialNoSensor,
    EmuVolumeSensor,
)
from homeassistant.core import HomeAssistant


class Gwf_water_2val(EmuCoordinator):
    """Coordinator for a 2 Value Water sensor."""

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
        """Create a new Coordinator object for a 2 Value Water sensor."""
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

        _LOGGER = logging.getLogger(__name__)
        _LOGGER.error("Initializing with given name %s", sensor_given_name)
        _LOGGER.error("caller name: %s", inspect.stack()[1][3])

        super().__init__(
            hass=hass,
            config_entry_id=config_entry_id,
            logger=logger,
            sensor_id=sensor_id,
            serial_no=serial_no,
            center_name=center_name,
            sensor_given_name=sensor_given_name,
        )
        self._sensors = [
            {
                "name": SERIAL_NO,
                "position": 0,
                "has_scaling_factor": False,
                "unit_str": "None",
                "description_str": "Fabrication",
                "sensor_class": EmuSerialNoSensor,
            },
            {
                "name": VOLUME,
                "position": 1,
                "has_scaling_factor": False,
                "unit_str": "m³",
                "description_str": "Volume",
                "sensor_class": EmuVolumeSensor,
            },
        ]

    @property
    def version_number(self) -> int:
        """Get the Version number of this device."""
        return 60

    @property
    def sensor_count(self) -> int:
        """Get the sensor count."""
        return 2

    @property
    def model_name(self) -> str:
        """Get the model name."""
        return "Water"

    @property
    def manufacturer_name(self) -> str:
        """Get the manufacturer name."""
        return "GWF"
