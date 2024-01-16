"""Platform for sensor integration."""
from __future__ import annotations

import abc
import logging
from datetime import timedelta
from typing import Any

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor import SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import POWER_VOLT_AMPERE_REACTIVE
from homeassistant.const import UnitOfApparentPower
from homeassistant.const import UnitOfElectricCurrent
from homeassistant.const import UnitOfElectricPotential
from homeassistant.const import UnitOfEnergy
from homeassistant.const import UnitOfFrequency
from homeassistant.const import UnitOfPower
from homeassistant.core import callback
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import CFG_FACTOR
from .const import CFG_PHASE
from .const import CFG_TARIFF
from .const import DOMAIN
from .const import SCALE_MANTISSA
from .const import SCALE_POWER
from .const import TARIFF
from .const import TIMESTAMP
from .device_types.devices import get_class_from_enum
from .emu_client import EmuApiClient

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    sensors_from_config = config_entry.data["sensors"]
    center_name = config_entry.data["name"]
    all_sensors = []
    for (
        sensor_id,
        serial_no,
        given_name,
        device_type,
    ) in sensors_from_config:
        coordinator = get_class_from_enum(device_type)(
            hass=hass,
            config_entry_id=config_entry.entry_id,
            logger=_LOGGER,
            sensor_id=sensor_id,
            serial_no=serial_no,
            center_name=center_name,
            sensor_given_name=given_name,
        )
        sensors = coordinator.sensors()
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
            manufacturer=self.coordinator.manufacturer_name,
            connections={(self.coordinator.center_name, self.coordinator.sensor_id)},
            sw_version=self.coordinator.version_number,
            configuration_url=f"http://{self.coordinator.ip}/app/",
            model=self.coordinator.model_name,
        )
        return info

    @property
    def unique_id(self) -> str | None:
        return f"Emu Sensor - {self._name} - {self._suffix}"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # _LOGGER.error(f"updating {self._suffix}")
        # _LOGGER.error(f"data: {self.coordinator.data}")
        item = next(
            item for item in self.coordinator.data if item.get("name") == self._suffix
        )
        self._attr_native_value = item.pop("value")
        del item["name"]
        self._attr_extra_state_attributes = item
        self.async_write_ha_state()


class EmuActiveEnergySensor(EmuBaseSensor):
    """Sensor for active energy in kWh"""

    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_icon = "mdi:lightning-bolt"


class EmuActiveEnergyResettableSensor(EmuBaseSensor):
    """Sensor for active energy in kWh that may be reset"""

    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_state_class = SensorStateClass.TOTAL
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_icon = "mdi:lightning-bolt"


class EmuActivePowerSensor(EmuBaseSensor):
    """Sensor for active power in kW"""

    _attr_native_unit_of_measurement = UnitOfPower.KILO_WATT
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_device_class = SensorDeviceClass.POWER
    _attr_icon = "mdi:lightning-bolt-circle"


class EmuVoltageSensor(EmuBaseSensor):
    """Sensor for Voltage in V"""

    _attr_native_unit_of_measurement = UnitOfElectricPotential.VOLT
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_device_class = SensorDeviceClass.VOLTAGE
    _attr_icon = "mdi:lightning-bolt"


class EmuCurrentSensor(EmuBaseSensor):
    """Sensor for the Current in A"""

    _attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_device_class = SensorDeviceClass.CURRENT
    _attr_icon = "mdi:flash-triangle"


class EmuFrequencySensor(EmuBaseSensor):
    """Sensor for the Grid frequency in Hz"""

    _attr_native_unit_of_measurement = UnitOfFrequency.HERTZ
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_device_class = SensorDeviceClass.FREQUENCY
    _attr_icon = "mdi:sine-wave"


class EmuTransformerFactorSensor(EmuBaseSensor):
    """Sensor for factor of the current transformer"""

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:close-outline"


class EmuErrorSensor(EmuBaseSensor):
    """sensor for the Error on the physical emu appliance"""

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:alert-circle-outline"


class EmuReactivePowerSensor(EmuBaseSensor):
    """Sensor for reactive power in VAr
    Yes, I would love to do it in kVAr, but that's not a thing in HA"""

    _attr_native_unit_of_measurement = POWER_VOLT_AMPERE_REACTIVE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_device_class = SensorDeviceClass.POWER
    _attr_icon = "mdi:glass-mug-variant"


class EmuReactiveEnergySensor(EmuBaseSensor):
    """Sensor for reactive energy in kVArh
    Sadly, varh and kvarh do not exist in HA"""

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_icon = "mdi:lightning-bolt-outline"


class EmuApparentPowerSensor(EmuBaseSensor):
    """Sensor for apparent power in VA
    Again, I would love to do it in kVA, but that's not a thing in HA"""

    _attr_native_unit_of_measurement = UnitOfApparentPower.VOLT_AMPERE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_device_class = SensorDeviceClass.POWER
    _attr_icon = "mdi:beer"


class EmuFormFactorSensor(EmuBaseSensor):
    """Sensor for form factor
    The Unit is Cos Phi, but that's not a thing in HA"""

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:sine-wave"


class EmuPowerFailureSensor(EmuBaseSensor):
    """Sensor for number of power failures"""

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:flash-off"


class EmuSerialNoSensor(EmuBaseSensor):
    """Sensor for the serial number of the sensor"""

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:barcode"


class EmuCoordinator(DataUpdateCoordinator, metaclass=abc.ABCMeta):
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
        self._config = dict(
            self._hass.config_entries.async_get_entry(self._config_entry_id).data
        )

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

    @property
    def ip(self):
        return self._config["ip"]

    @property
    def sensor_id(self):
        return self._sensor_id

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

    def sensors(self) -> list[EmuBaseSensor]:
        """Get all the Sensors this device Offers"""
        return [
            sensor["sensor_class"](self, sensor["name"]) for sensor in self._sensors
        ]

    def parse(self, data: list[dict]) -> list[dict]:
        """Parses the "ValueDescs" part of the Output of the API to a Dict, matching the correct values"""
        return [
            self._extract_values(
                data=data,
                position=sensor["position"],
                name=sensor["name"],
                has_scaling_factor=sensor["has_scaling_factor"],
                unit_str=sensor["unit_str"],
                description_str=sensor["description_str"],
            )
            for sensor in self._sensors
        ]

    def _extract_values(
        self,
        data: list[dict],
        position: int,
        name: str,
        has_scaling_factor: bool,
        unit_str: str,
        description_str: str | None,
    ) -> dict:
        """Extracts the values from the dict in the API response"""
        item = next(item for item in data if item["Position"] == position)
        # test if we found the right entry for active_energy_tariff_1
        if not (
            item["UnitStr"] == unit_str
            and (description_str is None or item["DescriptionStr"] == description_str)
        ):
            raise ValueError(
                f"Did not find the required Fields for {name} in the JSON response from the "
                "M-Bus Center"
            )
        result = {
            "name": name,
            "value": float(item["LoggerLastValue"]),
            SCALE_POWER: float(item.get("ScalePower")),
            SCALE_MANTISSA: int(item.get("ScaleMantissa")),
            TARIFF: int(item.get("Tariff")),
            CFG_PHASE: int(item.get("CfgPhase")),
            CFG_FACTOR: float(item.get("CfgFactor")),
            CFG_TARIFF: int(item.get("CfgTariff")),
            TIMESTAMP: int(item.get("Values")[0].get("Timestamp")),
        }
        if has_scaling_factor:
            result["value"] = result["value"] / (
                float(item.get("CfgFactor", 1)) if item.get("CfgFactor", 1) != 0 else 1
            )
        return result

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API endpoint.
        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """

        self.update_interval = timedelta(seconds=60)

        async def fetch_all_values() -> dict[str, float]:
            client = EmuApiClient(self.ip, self)
            data = await client.read_sensor_async(
                hass=self._hass, sensor_id=self._sensor_id
            )
            return data

        return await fetch_all_values()
