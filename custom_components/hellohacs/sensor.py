from homeassistant.helpers.entity import Entity
import asyncio

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the sensor platform."""
    async_add_entities([ExampleSensor(hass)])

class ExampleSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass):
        self._state = 0
        self._hass = hass
        self._hass.loop.create_task(self._increment_value())

    @property
    def name(self):
        return "Example Sensor"

    @property
    def state(self):
        return self._state

    async def _increment_value(self):
        """Increment the sensor value every second."""
        while True:
            self._state += 1
            self.async_write_ha_state()
            await asyncio.sleep(1)

