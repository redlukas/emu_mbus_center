"""Platform for sensor integration."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor import SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ELECTRIC_CURRENT_AMPERE
from homeassistant.const import ELECTRIC_POTENTIAL_VOLT
from homeassistant.const import FREQUENCY_HERTZ
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

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=60)


async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
):
    sensors_from_config = config_entry.data["sensors"]
    center_name = config_entry.data["name"]
    all_sensors = []
    for sensor_id, serial_no, given_name in sensors_from_config:
        coordinator = EmuCoordinator(
            hass=hass,
            config_entry_id=config_entry.entry_id,
            logger=_LOGGER,
            sensor_id=int(sensor_id),
            serial_no=serial_no,
            center_name=center_name,
            sensor_given_name=given_name,
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

    def __init__(self, coordinator: EmuCoordinator, suffix: str):
        SensorEntity.__init__(self)
        CoordinatorEntity.__init__(self, coordinator)
        self._name = coordinator.name
        self._suffix = suffix
        self._serial_no = coordinator.serial_no
        _LOGGER.debug(f"created Sensor of class {__class__} with uid {self.unique_id}")

    _attr_has_entity_name: True
    _attr_should_poll: True

    @property
    def name(self) -> str | None:
        return f"{self._name} {self._suffix}"

    @property
    def friendly_name(self) -> str | None:
        return f"{self._name} {self._suffix.replace('_', ' ').capitalize()}"

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        info = DeviceInfo(
            identifiers={(DOMAIN, self._name)},
            name=f"{self._name}",
            manufacturer="EMU", # TODO: See if we can get that from the API
            model="EMU Allrounder 75/3", # TODO: See if we can get that from the API
            connections={(self.coordinator.center_name, self._serial_no)},
            sw_version="1.0.0", # TODO: get the version from the API
            configuration_url=f"http://10.100.70.184/app/" # TODO: get the IP of the center from the config
        )
        return info

    @property
    def unique_id(self) -> str | None:
        return f"Emu Sensor - {self._name} - {self._suffix}"

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

        super().__init__(
            hass=hass,
            logger=logger,
            name=self._name,
            update_interval=timedelta(seconds=60),
        )

    @property
    def get_hass(self):
        return self._hass

    @property
    def config_entry_id(self):
        return self._config_entry_id

    @property
    def serial_no(self):
        return self._serial_no

    @property
    def center_name(self):
        return self._center_name

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API endpoint.
        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        config = dict(
            self._hass.config_entries.async_get_entry(self._config_entry_id).data
        )

        self.update_interval = timedelta(seconds=60)

        async def fetch_all_values() -> dict[str, float]:
            client = EmuApiClient(config["ip"])
            data = await client.read_sensor_async(
                hass=self._hass, sensor_id=self._sensor_id
            )
            return data

        return await fetch_all_values()
