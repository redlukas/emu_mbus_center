"""Platform for sensor integration."""
from __future__ import annotations

import json
import logging
from datetime import timedelta
from typing import Any

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor import SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_IP_ADDRESS
from homeassistant.const import CONF_UNIQUE_ID
from homeassistant.const import ELECTRIC_CURRENT_AMPERE
from homeassistant.const import ELECTRIC_POTENTIAL_VOLT
from homeassistant.const import FREQUENCY_HERTZ
from homeassistant.const import STATE_UNAVAILABLE
from homeassistant.const import UnitOfEnergy
from homeassistant.const import UnitOfPower
from homeassistant.core import callback
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import ACTIVE_ENERGY_TARIFF_1
from .const import ACTIVE_ENERGY_TARIFF_2
from .const import ACTIVE_POWER_ALL_PHASES
from .const import ACTIVE_POWER_PHASE_1
from .const import ACTIVE_POWER_PHASE_2
from .const import ACTIVE_POWER_PHASE_3
from .const import CURRENT_ALL_PHASES
from .const import CURRENT_PHASE_1
from .const import CURRENT_PHASE_2
from .const import CURRENT_PHASE_3
from .const import CURRENT_TRANSFORMER_FACTOR
from .const import DOMAIN
from .const import ERROR_FLAGS
from .const import FREQUENCY
from .const import RESET_COUNTER
from .const import VOLTAGE_PHASE_1
from .const import VOLTAGE_PHASE_2
from .const import VOLTAGE_PHASE_3
from .emu_client import EmuApiClient
from .emu_client import EmuApiError

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=60)

# Validation of the user's config
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_IP_ADDRESS): cv.string,
        vol.Required(CONF_UNIQUE_ID): cv.ensure_list,
    }
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    parsed = json.loads(config_entry.data["sensors"])
    all_sensors = []
    for name, sensor_id in parsed.items():
        coordinator = EmuCoordinator(
            hass=hass,
            config_entry_id=config_entry.entry_id,
            logger=_LOGGER,
            name=name,
            sensor_id=int(sensor_id),
        )
        sensors = [
            EmuEnergySensor(coordinator, ACTIVE_ENERGY_TARIFF_1),
            EmuEnergySensor(coordinator, ACTIVE_ENERGY_TARIFF_2),
            EmuPowerSensor(coordinator, ACTIVE_POWER_PHASE_1),
            EmuPowerSensor(coordinator, ACTIVE_POWER_PHASE_2),
            EmuPowerSensor(coordinator, ACTIVE_POWER_PHASE_3),
            EmuPowerSensor(coordinator, ACTIVE_POWER_ALL_PHASES),
            EmuVoltageSensor(coordinator, VOLTAGE_PHASE_1),
            EmuVoltageSensor(coordinator, VOLTAGE_PHASE_2),
            EmuVoltageSensor(coordinator, VOLTAGE_PHASE_3),
            EmuCurrentSensor(coordinator, CURRENT_PHASE_1),
            EmuCurrentSensor(coordinator, CURRENT_PHASE_2),
            EmuCurrentSensor(coordinator, CURRENT_PHASE_3),
            EmuCurrentSensor(coordinator, CURRENT_ALL_PHASES),
            EmuFrequencySensor(coordinator, FREQUENCY),
            EmuResetSensor(coordinator, RESET_COUNTER),
            EmuTransformerFactorSensor(coordinator, CURRENT_TRANSFORMER_FACTOR),
            EmuErrorSensor(coordinator, ERROR_FLAGS),
        ]

        all_sensors.extend(sensors)
        await coordinator.async_config_entry_first_refresh()
    async_add_entities(all_sensors)


class EmuBaseSensor(CoordinatorEntity, SensorEntity):
    """base Emu Sensor, all sensors inherit from it"""

    def __init__(self, coordinator: DataUpdateCoordinator, suffix: str):
        SensorEntity.__init__(self)
        CoordinatorEntity.__init__(self, coordinator)
        self._name = coordinator.name
        self._suffix = suffix

    @property
    def name(self) -> str | None:
        return f"{self._name} {self._suffix}"

    @property
    def should_poll(self) -> bool:
        return True

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={DOMAIN},
            name=f"Emu Sensor-{self._name}-{self._suffix}",
            manufacturer="EMU",
            model="EMU M-Bus Center",
        )

    _attr_has_entity_name: True

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        value = self.coordinator.data[self._suffix]
        self._attr_native_value = value
        self.async_write_ha_state()


class EmuEnergySensor(EmuBaseSensor):
    """Sensor for active energy in kWh"""

    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_icon = "mdi:lightning-bolt"


class EmuPowerSensor(EmuBaseSensor):
    """Sensor for active power in kW"""

    _attr_native_unit_of_measurement = UnitOfPower.KILO_WATT
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_device_class = SensorDeviceClass.POWER
    _attr_icon = "mdi:lightning-bolt-circle"


class EmuVoltageSensor(EmuBaseSensor):
    """Sensor for Voltage in V"""

    _attr_native_unit_of_measurement = ELECTRIC_POTENTIAL_VOLT
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_device_class = SensorDeviceClass.VOLTAGE
    _attr_icon = "mdi:lightning-bolt"


class EmuCurrentSensor(EmuBaseSensor):
    """Sensor for the Current in A"""

    _attr_native_unit_of_measurement = ELECTRIC_CURRENT_AMPERE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_device_class = SensorDeviceClass.CURRENT
    _attr_icon = "mdi:flash-triangle"


class EmuFrequencySensor(EmuBaseSensor):
    """Sensor for the Grid frequency in Hz"""

    _attr_native_unit_of_measurement = FREQUENCY_HERTZ
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_device_class = SensorDeviceClass.FREQUENCY
    _attr_icon = "mdi:sine-wave"


class EmuResetSensor(EmuBaseSensor):
    """Sensor for the number of Resets"""

    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_icon = "mdi:lock-reset"


class EmuTransformerFactorSensor(EmuBaseSensor):
    """Sensor for factor of the current transformer"""

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:close-outline"


class EmuErrorSensor(EmuBaseSensor):
    """sensor for the Error on the physical emu appliance"""

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:alert-circle-outline"


class EmuCoordinator(DataUpdateCoordinator):
    """Custom M-Bus Center Coordinator"""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry_id: str,
        logger: logging.Logger,
        name: str,
        sensor_id: int,
    ) -> None:
        _LOGGER.error(f"initializing Coordinator for {name}")
        self._config_entry_id = config_entry_id
        self._hass = hass
        self._name = name
        self._sensor_id = sensor_id
        self._logger = logger

        super().__init__(
            hass,
            logger,
            name=name,
            update_interval=timedelta(seconds=60),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API endpoint.
        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        config = dict(
            self._hass.config_entries.async_get_entry(self._config_entry_id).data
        )

        self.update_interval = timedelta(seconds=60)

        def _safe_fetch(func: callable, num_ret: int, *args, **kwargs):
            if num_ret == 1:
                ret = STATE_UNAVAILABLE
            else:
                ret = [STATE_UNAVAILABLE] * num_ret

            try:
                ret = func(*args, **kwargs)
            except EmuApiError as err:
                _LOGGER.error(
                    "Error fetching data in coordinator: function %s, %s",
                    func.__name__,
                    err,
                )

            if num_ret == 1:
                # only one return value
                return ret
            if len(ret) != num_ret:
                raise ValueError(
                    f"Number of return args doesn't match, expected: {num_ret}, got: {len(ret)}"
                )
            return ret

        async def fetch_all_values() -> dict[str, float]:
            client = EmuApiClient(config["ip"])
            data = await client.read_sensor_async(
                hass=self._hass, sensor_id=self._sensor_id
            )
            # self._logger.error(f"data returnig from update is {data}")
            return data

        return await fetch_all_values()


# def setup_platform(
#         hass: HomeAssistant,
#         config: ConfigType,
#         add_entities: AddEntitiesCallback,
#         discovery_info: DiscoveryInfoType | None = None,
# ) -> None:
#     """Set up the sensor platform."""
#     for entry in config[CONF_UNIQUE_ID]:
#         item = entry.popitem(True)
#         sensor = {"name": item[0], "ip_address": config[CONF_IP_ADDRESS], "id": item[1]}
#         add_entities([EmuMBusCenterSensor(sensor)], True)
#         """The "true" argument assures the values get fetched before the first write to HA"""


class EmuMBusCenterSensor(SensorEntity):
    """emu_m_bus_center Sensor class."""

    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_has_entity_name: True
    _attr_icon = "mdi:lightning-bolt"
    _attr_should_poll: True

    def __init__(self, sensor) -> None:
        self._name = sensor["name"]
        self._ip = sensor["ip_address"]
        self._id = sensor["id"]

    @property
    def name(self) -> str:
        """Return the display name of this sensor."""
        return self._name
