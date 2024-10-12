import inspect
import logging

from custom_components.emu_m_bus_center.const import SERIAL_NO
from custom_components.emu_m_bus_center.const import VOLUME
from custom_components.emu_m_bus_center.sensor import EmuCoordinator
from custom_components.emu_m_bus_center.sensor import EmuSerialNoSensor
from custom_components.emu_m_bus_center.sensor import EmuVolumeSensor
from homeassistant.core import HomeAssistant


class Gwf_water_2val(EmuCoordinator):
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

        _LOGGER = logging.getLogger(__name__)
        _LOGGER.error(f"Initializing with given name {sensor_given_name}")
        _LOGGER.error("caller name:", inspect.stack()[1][3])

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
        return 60

    @property
    def sensor_count(self) -> int:
        return 2

    @property
    def model_name(self) -> str:
        return "Water"

    @property
    def manufacturer_name(self) -> str:
        return "GWF"
