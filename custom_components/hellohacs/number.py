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
from homeassistant.const import PERCENTAGE, UnitOfPower
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

@dataclass
class HuaweiSolarNumberEntityDescription(NumberEntityDescription):
    """Describes Huawei Solar number entity."""

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Huawei Solar Number entities Setup."""

    entities_to_add: list[NumberEntity] = []

    entities_to_add.append(
        HuaweiSolarNumberEntity(
            HuaweiSolarNumberEntityDescription(
                key="huawei_solar_battery_soc",
                name="Battery State of Charge",
                native_min_value=DEFAULT_MIN_VALUE,
                native_max_value=DEFAULT_MAX_VALUE,
                native_unit_of_measurement=PERCENTAGE,
                mode=NumberMode.AUTO,
            ),
            native_value=50,
        )
    )

    async_add_entities(entities_to_add)

class HuaweiSolarNumberEntity(NumberEntity):
    """Representation of a Huawei Solar number entity."""

    def __init__(self, description: HuaweiSolarNumberEntityDescription, native_value: float):
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