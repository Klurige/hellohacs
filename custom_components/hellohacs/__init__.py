from homeassistant import core


async def async_setup(hass: core.HomeAssistant, config: dict) -> bool:
    """Set up the Hello Hacs component."""
    # @TODO: Add setup code.
    return True

async def async_setup_entry(hass, entry):
    """Set up hellohacs from a config entry."""
    # Perform any setup tasks here
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Example: Set up a platform
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )

    return True
