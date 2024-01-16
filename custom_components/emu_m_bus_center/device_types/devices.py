from enum import Enum
from typing import Type
from typing import Union

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator


class Device_type(Enum):
    ALLROUNDER_v16_15val = "EMU Allrounder | Firmware Version 16 | 15 Values"
    ALLROUNDER_v16_17val = "EMU Allrounder | Firmware Version 16 | 17 Values"
    PROFESSIONAL_v16_31val = "EMU Professional | Firmware Version 16 | 31 Values"
    PROFESSIONAL_v16_32val = "EMU Professional | Firmware Version 16 | 32 Values"
    EMU_1_40_v4_15val = "EMU 1/40 | Firmware Version 4 | 15 Values"


def get_class_from_enum(
    enum_or_str: Union[Device_type, str]
) -> Type[DataUpdateCoordinator] | None:
    """You input a device type enum, you get the corresponding Class object
    Sice we have to expect a whole host of different python versions, you may even input a string
    and it will be converted to the corresponding enum value"""
    from custom_components.emu_m_bus_center.device_types.emu_allrounder_v16_17val import (
        EmuAllrounderV16_17val,
    )
    from custom_components.emu_m_bus_center.device_types.emu_allrounder_v16_15val import (
        EmuAllrounderV16_15val,
    )
    from custom_components.emu_m_bus_center.device_types.emu_professional_v16_31val import (
        EmuProfessionalV16_31val,
    )
    from custom_components.emu_m_bus_center.device_types.emu_professional_v16_32val import (
        EmuProfessionalV16_32val,
    )

    from custom_components.emu_m_bus_center.device_types.emu_1_40_v4_15val import (
        Emu_1_40_V4_15val,
    )
    from custom_components.emu_m_bus_center.emu_client import EmuApiError

    template_mapping = {
        Device_type.ALLROUNDER_v16_15val: EmuAllrounderV16_15val,
        Device_type.ALLROUNDER_v16_17val: EmuAllrounderV16_17val,
        Device_type.PROFESSIONAL_v16_31val: EmuProfessionalV16_31val,
        Device_type.PROFESSIONAL_v16_32val: EmuProfessionalV16_32val,
        Device_type.EMU_1_40_v4_15val: Emu_1_40_V4_15val,
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
    """You have a version number and you know how many sensor values you get from the API, but you don't know what
    device this is? Boy, do I have the right method for you!"""
    device_type_matrix = {
        (4, 15): Device_type.EMU_1_40_v4_15val,
        (16, 15): Device_type.ALLROUNDER_v16_15val,
        (16, 17): Device_type.ALLROUNDER_v16_17val,
        (16, 31): Device_type.PROFESSIONAL_v16_31val,
        (16, 32): Device_type.PROFESSIONAL_v16_32val,
    }
    return device_type_matrix.get((version, sensor_count), None)
