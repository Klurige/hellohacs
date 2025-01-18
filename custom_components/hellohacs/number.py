from __future__ import annotations

from dataclasses import dataclass
import logging

from homeassistant.components.number import (
    NumberEntity,
    NumberEntityDescription,
    NumberMode,
)
from homeassistant.components.number.const import DEFAULT_MAX_VALUE, DEFAULT_MIN_VALUE
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

@dataclass
class ElectricityPriceLevelsNumberEntityDescription(NumberEntityDescription):
    """Describes ElectricityPriceLevels number entities."""

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the ElectricityPriceLevels number entities."""

    device_info = DeviceInfo(
        identifiers={(DOMAIN, entry.entry_id)},
        name="Electricity Price Levels Device",
        manufacturer="Your Manufacturer",
        model="Your Model",
        sw_version="1.0",
    )

    entities_to_add: list[NumberEntity] = []

    entities_to_add.append(
        ElectricityPriceLevelsNumberEntity(
            ElectricityPriceLevelsNumberEntityDescription(
                key="electricity_price_levels_supplier_balance_fee",
                name="Electricity Supplier Balance Fee",
                native_min_value=DEFAULT_MIN_VALUE,
                native_max_value=DEFAULT_MAX_VALUE,
                native_unit_of_measurement="öre/kWh",
                mode=NumberMode.BOX,
                entity_category=EntityCategory.CONFIG,
            ),
            native_value=2.92,
            device_info=device_info,
        )
    )

    async_add_entities(entities_to_add)

class ElectricityPriceLevelsNumberEntity(NumberEntity):
    """Representation of an ElectricityPriceLevels number entity."""

    def __init__(self, description: ElectricityPriceLevelsNumberEntityDescription, native_value: float, device_info: DeviceInfo):
        self.entity_description = description
        self._attr_native_value = native_value
        self._attr_device_info = device_info

    @property
    def native_value(self) -> float:
        """Return the current value."""
        return self._attr_native_value

    @native_value.setter
    def native_value(self, value: float) -> None:
        """Set the current value."""
        self._attr_native_value = value