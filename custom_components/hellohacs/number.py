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
from homeassistant.helpers.entity_platform import AddEntitiesCallback

_LOGGER = logging.getLogger(__name__)


@dataclass
class ElectricityPriceLevelsNumberEntityDescription(NumberEntityDescription):
    """ Describes ElectritiyPriceLevels nuber entities."""


async def async_setup_entry(
        hass: HomeAssistant,
        entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the ElectricityPriceLevels number entities."""

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
                entity_category="Electricity Price Levels",
            ),
            native_value=2.92,
        )
    )

    async_add_entities(entities_to_add)


class ElectricityPriceLevelsNumberEntity(NumberEntity):
    """Representation of a ElectricityPriceLevels number entity."""

    def __init__(self, description: ElectricityPriceLevelsNumberEntityDescription, native_value: float):
        self.entity_description = description
        self._attr_native_value = native_value

    @property
    def native_value(self) -> float:
        """Return the current value."""
        return self._attr_native_value

    @native_value.setter
    def native_value(self, value: float) -> None:
        """Set the current value."""
        self._attr_native_value = value
