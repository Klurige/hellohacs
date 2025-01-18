from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.number import NumberEntity
from homeassistant.helpers.entity import Entity
from .const import DOMAIN
from homeassistant.const import Platform

PLATFORMS: list[Platform] = [
    Platform.NUMBER,
    Platform.SENSOR
]

class ExampleNumberEntity(NumberEntity):
    def __init__(self, hass, name, initial, min_value, max_value, step):
        self.hass = hass
        self._name = name
        self._state = initial
        self._min_value = min_value
        self._max_value = max_value
        self._step = step

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def min_value(self):
        return self._min_value

    @property
    def max_value(self):
        return self._max_value

    @property
    def step(self):
        return self._step

    async def async_set_value(self, value):
        self._state = value
        self.async_write_ha_state()

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> bool:
    """Set up hellohacs from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Create the number entity
    number_entity = ExampleNumberEntity(
        hass,
        name="Example Slider",
        initial=30,
        min_value=0,
        max_value=100,
        step=1
    )

    # Register the entity
    async_add_entities([number_entity])

    # Await the async_forward_entry_setup call
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Perform any cleanup tasks here
    if entry.entry_id in hass.data[DOMAIN]:
        hass.data[DOMAIN].pop(entry.entry_id)

    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)