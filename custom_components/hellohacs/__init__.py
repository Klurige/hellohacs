from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_component import EntityComponent
from .const import DOMAIN
from homeassistant.const import Platform

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up hellohacs from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data


    # Create the input_number entity
    input_number = InputNumber(
        hass,
        name="Example Slider",
        initial=30,
        min_value=0,
        max_value=100,
        step=1
    )

    # Register the entity
    component = hass.data.get("entity_components", {}).get("input_number")
    if component is None:
        component = EntityComponent(hass, "input_number", hass.data[DOMAIN])
        hass.data["entity_components"]["input_number"] = component

    await component.async_add_entities([input_number])

    # Await the async_forward_entry_setup call
    await hass.config_entries.async_forward_entry_setups(entry, [Platform.SENSOR, Platform.NUMBER])

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Perform any cleanup tasks here
    if entry.entry_id in hass.data[DOMAIN]:
        hass.data[DOMAIN].pop(entry.entry_id)

    return await hass.config_entries.async_forward_entry_unload(entry, "sensor")


