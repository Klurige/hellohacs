"""Number entities for Huawei Solar."""

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
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class HuaweiSolarNumberEntityDescription(NumberEntityDescription):
    """Huawei Solar Number Entity Description."""
    static_minimum_key: str | None = None
    static_maximum_key: str | None = None

    def __post_init__(self):
        """Defaults the translation_key to the number key."""
        # We use this special setter to be able to set/update the translation_key
        # in this frozen dataclass.
        # cfr. https://docs.python.org/3/library/dataclasses.html#frozen-instances
        object.__setattr__(
            self,
            "translation_key",
            self.translation_key or self.key.replace("#", "_").lower(),
        )

    @property
    def context(self):
        """Context used by DataUpdateCoordinator."""

        registers = [self.key]
        return {"register_names": registers}


INVERTER_NUMBER_DESCRIPTIONS: tuple[HuaweiSolarNumberEntityDescription, ...] = (
    HuaweiSolarNumberEntityDescription(
        key="ACTIVE_POWER_PERCENTAGE_DERATING",
        native_max_value=100,
        native_step=0.1,
        native_min_value=-100,
        icon="mdi:transmission-tower-off",
        native_unit_of_measurement=PERCENTAGE,
        entity_category=EntityCategory.CONFIG,
    ),
    HuaweiSolarNumberEntityDescription(
        key="ACTIVE_POWER_FIXED_VALUE_DERATING",
        static_maximum_key=100,
        native_step=1,
        native_min_value=0,
        icon="mdi:transmission-tower",
        native_unit_of_measurement=UnitOfPower.WATT,
        entity_category=EntityCategory.CONFIG,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Huawei Solar Number entities Setup."""

    entities_to_add: list[NumberEntity] = []
    slave_entities: list[HuaweiSolarNumberEntity] = []
    for entity_description in INVERTER_NUMBER_DESCRIPTIONS:
        slave_entities.append(  # noqa: PERF401
            await HuaweiSolarNumberEntity.create(
                entity_description
            )
        )


    entities_to_add.extend(slave_entities)

    async_add_entities(entities_to_add)


class HuaweiSolarNumberEntity(NumberEntity):
    """Huawei Solar Number Entity."""

    entity_description: HuaweiSolarNumberEntityDescription
    _attr_mode = NumberMode.BOX  # Always allow a precise number

    _static_min_value: float | None = None
    _static_max_value: float | None = None

    _dynamic_min_value: float | None = None
    _dynamic_max_value: float | None = None

    def __init__(
        self,
        description: HuaweiSolarNumberEntityDescription,
        static_max_value: float | None = None,
        static_min_value: float | None = None,
    ) -> None:
        """Huawei Solar Number Entity constructor.

        Do not use directly. Use `.create` instead!
        """
        super().__init__(description.context)
        self.entity_description = description
        self._attr_unique_id = f"{description.key}"

        self._static_max_value = static_max_value
        self._static_min_value = static_min_value

    @classmethod
    async def create(
        cls,
        description: HuaweiSolarNumberEntityDescription,
    ) -> HuaweiSolarNumberEntity:
        """Huawei Solar Number Entity constructor.

        This async constructor fills in the necessary min/max values
        """

        static_max_value = None

        static_min_value = None

        return cls(
            description,
            static_max_value,
            static_min_value,
        )

