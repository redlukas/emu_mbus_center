"""Help keep track of all the different device types we know about."""

from dataclasses import dataclass
from enum import Enum
import logging

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class Device_type(Enum):
    """Hold all the different device types we know about."""

    ALLROUNDER_v16_15val = "EMU Allrounder | Firmware Version 16 | 15 Values"
    ALLROUNDER_v16_17val = "EMU Allrounder | Firmware Version 16 | 17 Values"
    PROFESSIONAL_v16_31val = "EMU Professional | Firmware Version 16 | 31 Values"
    PROFESSIONAL_v16_32val = "EMU Professional | Firmware Version 16 | 32 Values"
    PROFESSIONAL_v25_24val = "EMU Professional | Firmware Version 25 | 24 Values"
    EMU_1_40_v4_15val = "EMU 1/40 | Firmware Version 4 | 15 Values"
    GWF_WATER_2val = "GWF Water Meter | 2 Values"


def get_class_from_enum(
    enum_or_str: Device_type | str,
) -> type[DataUpdateCoordinator] | None:
    """Get class from enum.

    You input a device type enum, you get the corresponding Class object
    Sice we have to expect a whole host of different python versions,
    you may even input a string
    and it will be converted to the corresponding enum value
    """
    # ruff: noqa: PLC0415
    from custom_components.emu_m_bus_center.device_types.emu_1_40_v4_15val import (
        Emu_1_40_V4_15val,
    )
    from custom_components.emu_m_bus_center.device_types.emu_allrounder_v16_15val import (
        EmuAllrounderV16_15val,
    )
    from custom_components.emu_m_bus_center.device_types.emu_allrounder_v16_17val import (
        EmuAllrounderV16_17val,
    )
    from custom_components.emu_m_bus_center.device_types.emu_professional_v16_31val import (
        EmuProfessionalV16_31val,
    )
    from custom_components.emu_m_bus_center.device_types.emu_professional_v16_32val import (
        EmuProfessionalV16_32val,
    )
    from custom_components.emu_m_bus_center.device_types.emu_professional_v25_24val import (
        EmuProfessionalV25_24val,
    )
    from custom_components.emu_m_bus_center.device_types.gwf_water_2val import (
        Gwf_water_2val,
    )
    from custom_components.emu_m_bus_center.emu_client import EmuApiError

    template_mapping = {
        Device_type.ALLROUNDER_v16_15val: EmuAllrounderV16_15val,
        Device_type.ALLROUNDER_v16_17val: EmuAllrounderV16_17val,
        Device_type.PROFESSIONAL_v16_31val: EmuProfessionalV16_31val,
        Device_type.PROFESSIONAL_v16_32val: EmuProfessionalV16_32val,
        Device_type.PROFESSIONAL_v25_24val: EmuProfessionalV25_24val,
        Device_type.EMU_1_40_v4_15val: Emu_1_40_V4_15val,
        Device_type.GWF_WATER_2val: Gwf_water_2val,
    }

    value_to_name = {e.value: e.name for e in Device_type}

    # If input is a string, determine if it's an enum name or enum value
    if isinstance(enum_or_str, str):
        if enum_or_str in Device_type.__members__:
            # Input string is an enum name
            enum_or_str = Device_type[enum_or_str]
        elif enum_or_str in value_to_name:
            # Input string is an enum value
            enum_or_str = Device_type[value_to_name[enum_or_str]]
        else:
            raise EmuApiError(f"Unknown device type {enum_or_str}")

    return template_mapping.get(enum_or_str)


def get_enum_from_version_and_sensor_count(
    version: int, sensor_count: int
) -> Device_type | None:
    """Map version number and sensor count to device type.

    You have a version number, and you know how many sensor values you get from the API, but you don't know what
    device this is? Boy, do I have the right method for you!
    """
    device_type_matrix = {
        (4, 15): Device_type.EMU_1_40_v4_15val,
        (16, 15): Device_type.ALLROUNDER_v16_15val,
        (16, 17): Device_type.ALLROUNDER_v16_17val,
        (16, 31): Device_type.PROFESSIONAL_v16_31val,
        (16, 32): Device_type.PROFESSIONAL_v16_32val,
        (25, 24): Device_type.PROFESSIONAL_v25_24val,
        (60, 2): Device_type.GWF_WATER_2val,
    }
    return device_type_matrix.get((version, sensor_count), None)


def get_supported_measurement_types() -> list[str]:
    """Get a list of all supported measurement types."""
    return ["Electricity", "Water"]


@dataclass
class Generic_sensor:
    """Class to hold info about an inspecific device."""

    sensor_id: int
    serial_number: int
    name: str
    device_type: Device_type

    @staticmethod
    def from_dict(data):
        """Create a generic_sensor object from a dict."""
        return Generic_sensor(
            sensor_id=data["sensor_id"],
            serial_number=data["serial_number"],
            name=data["name"],
            device_type=Device_type[data["device_type"]],
        )

    def to_dict(self):
        """Convert to dict."""
        return {
            "sensor_id": self.sensor_id,
            "serial_number": self.serial_number,
            "name": self.name,
            "device_type": self.device_type.name,
        }


def generic_sensor_deserializer(sensor_as_dict) -> Generic_sensor:
    """Convert the dict representation of a generic sensor into a generic sensor object."""
    if (
        "sensor_id" in sensor_as_dict
        and "serial_number" in sensor_as_dict
        and "name" in sensor_as_dict
        and "device_type" in sensor_as_dict
    ):
        return Generic_sensor.from_dict(sensor_as_dict)
    raise ValueError("Could not recognize generic sensor %s", sensor_as_dict)
