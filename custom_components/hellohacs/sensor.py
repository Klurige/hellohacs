"""Support for the Forecast.Solar sensor service."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

from homeassistant.components.sensor import (
    DOMAIN as SENSOR_DOMAIN,
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import UnitOfEnergy, UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN


@dataclass(frozen=True)
class ForecastSolarSensorEntityDescription(SensorEntityDescription):
    """Describes a Forecast.Solar Sensor."""


SENSORS: tuple[ForecastSolarSensorEntityDescription, ...] = (
    ForecastSolarSensorEntityDescription(
        key="energy_production_today",
        translation_key="energy_production_today",
        state=0,
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_display_precision=1,
    ),
    ForecastSolarSensorEntityDescription(
        key="energy_production_today_remaining",
        translation_key="energy_production_today_remaining",
        state=0,
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_display_precision=1,
    ),
    ForecastSolarSensorEntityDescription(
        key="energy_production_tomorrow",
        translation_key="energy_production_tomorrow",
        state=0,
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_display_precision=1,
    ),
    ForecastSolarSensorEntityDescription(
        key="power_highest_peak_time_today",
        translation_key="power_highest_peak_time_today",
        device_class=SensorDeviceClass.TIMESTAMP,
    ),
    ForecastSolarSensorEntityDescription(
        key="power_highest_peak_time_tomorrow",
        translation_key="power_highest_peak_time_tomorrow",
        device_class=SensorDeviceClass.TIMESTAMP,
    ),
    ForecastSolarSensorEntityDescription(
        key="power_production_now",
        translation_key="power_production_now",
        device_class=SensorDeviceClass.POWER,
        state=0,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),
    ForecastSolarSensorEntityDescription(
        key="power_production_next_hour",
        translation_key="power_production_next_hour",
        state=0,
        device_class=SensorDeviceClass.POWER,
        entity_registry_enabled_default=False,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),
    ForecastSolarSensorEntityDescription(
        key="power_production_next_12hours",
        translation_key="power_production_next_12hours",
        state=0,
        device_class=SensorDeviceClass.POWER,
        entity_registry_enabled_default=False,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),
    ForecastSolarSensorEntityDescription(
        key="power_production_next_24hours",
        translation_key="power_production_next_24hours",
        state=0,
        device_class=SensorDeviceClass.POWER,
        entity_registry_enabled_default=False,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),
    ForecastSolarSensorEntityDescription(
        key="energy_current_hour",
        translation_key="energy_current_hour",
        state=0,
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_display_precision=1,
    ),
    ForecastSolarSensorEntityDescription(
        key="energy_next_hour",
        translation_key="energy_next_hour",
        state=0,
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_display_precision=1,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Defer sensor setup to the shared sensor module."""
    coordinator = entry.runtime_data

    async_add_entities(
        ForecastSolarSensorEntity(
            entry_id=entry.entry_id,
            coordinator=coordinator,
            entity_description=entity_description,
        )
        for entity_description in SENSORS
    )


class ForecastSolarSensorEntity(SensorEntity
):
    """Defines a Forecast.Solar sensor."""

    entity_description: ForecastSolarSensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        *,
        entry_id: str,
        entity_description: ForecastSolarSensorEntityDescription,
    ) -> None:
        """Initialize Forecast.Solar sensor."""
        super().__init__()
        self.entity_description = entity_description
        self.entity_id = f"{SENSOR_DOMAIN}.{entity_description.key}"
        self._attr_unique_id = f"{entry_id}_{entity_description.key}"

        self._attr_device_info = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, entry_id)},
            manufacturer="Forecast.Solar",
            model=coordinator.data.account_type.value,
            name="Solar production forecast",
            configuration_url="https://forecast.solar",
        )

    @property
    def native_value(self) -> datetime | StateType:
        """Return the state of the sensor."""
        if self.entity_description.state is None:
            state: StateType | datetime = getattr(
                self.coordinator.data, self.entity_description.key
            )
        else:
            state = self.entity_description.state(self.coordinator.data)

        return state