from homeassistant.helpers.entity import Entity

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the sensor platform."""
    async_add_entities([ExampleSensor()])

class ExampleSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self):
        self._state = None

    @property
    def name(self):
        return "Example Sensor"

    @property
    def state(self):
        return self._state

    async def async_update(self):
        """Fetch new state data for the sensor."""
        self._state = "some_value"
