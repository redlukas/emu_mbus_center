import abc

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator


class Readable_device(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def version_number(self) -> int:
        """Get the Version number of this device"""

    @property
    @abc.abstractmethod
    def sensor_count(self) -> int:
        """Get how many sensors this device has"""

    @property
    @abc.abstractmethod
    def model_name(self) -> str:
        """Get the human-readable representation of the Device's model name"""

    @property
    @abc.abstractmethod
    def manufacturer_name(self) -> str:
        """Get the human-readable representation of the Device's manufacturer name"""

    @abc.abstractmethod
    def sensors(self, coordinator: DataUpdateCoordinator) -> list[str]:
        """Get all the Sensors this device Offers"""

    @abc.abstractmethod
    def parse(self, data: str) -> dict[str, float]:
        """Parses the Output of the API to a Dict, matching the correct values"""
