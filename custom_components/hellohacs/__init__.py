from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up hellohacs from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Create the input_number entity
    input_number_config = {
        "name": "Elhandel Balansavgift",
        "min": 0,
        "max": 100,
        "step": 0.001,
        "unit_of_measurement": "öre/kWh",
        "mode": "box"
    }
    input_number_entity_id = "input_number.supplier_balance_fee"
    entity_registry = er.async_get(hass)
    entity_registry.async_get_or_create(
        domain="input_number",
        platform="hellohacs",
        unique_id=input_number_entity_id,
        config_entry=entry,
        **input_number_config
    )


    # Await the async_forward_entry_setup call
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Perform any cleanup tasks here
    if entry.entry_id in hass.data[DOMAIN]:
        hass.data[DOMAIN].pop(entry.entry_id)

    return await hass.config_entries.async_forward_entry_unload(entry, "sensor")


