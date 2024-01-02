from enum import Enum

from custom_components.emu_m_bus_center.device_types.readable_device import (
    Readable_device,
)


class Device_type(Enum):
    ALLROUNDER_v16_17val = "EMU Allrounder | Firmware Version 16 | 17 Values"
    PROFESSIONAL_v16_31val = "EMU Professional | Firmware Version 16 | 31 Values"


def get_class_from_enum(enum: Device_type) -> Readable_device | None:
    """You input a device type enum, you get the corresponding Class object"""
    from custom_components.emu_m_bus_center.device_types.emu_allrounder_v16_17val import (
        EmuAllrounderV16_17val,
    )
    from custom_components.emu_m_bus_center.device_types.emu_professional_v16_31val import (
        EmuProfessionalV16_31val,
    )

    template_mapping = {
        Device_type.ALLROUNDER_v16_17val: EmuAllrounderV16_17val,
        Device_type.PROFESSIONAL_v16_31val: EmuProfessionalV16_31val,
    }
    return template_mapping.get(enum, None)()


def get_enum_from_version_and_sensor_count(
    version: int, sensor_count: int
) -> Device_type | None:
    """You have a version number and you know how many sensor values you get from the API, but you don't know what
    device this is? Boy, do I have the right method for you!"""
    device_type_matrix = {
        (16, 17): Device_type.ALLROUNDER_v16_17val,
        (16, 31): Device_type.PROFESSIONAL_v16_31val,
    }
    return device_type_matrix.get((version, sensor_count), None)
