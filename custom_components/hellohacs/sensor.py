from homeassistant.helpers.entity import Entity
from homeassistant.const import EVENT_STATE_CHANGED

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the sensor platform."""
    async_add_entities([ExampleSensor(hass, "sensor.other_sensor")])

class ExampleSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass, other_sensor_id):
        self._state = 0
        self._hass = hass
        self._other_sensor_id = other_sensor_id
        self._hass.bus.async_listen(EVENT_STATE_CHANGED, self._handle_event)

    @property
    def name(self):
        return "Example Sensor"

    @property
    def state(self):
        return self._state

    async def _handle_event(self, event):
        """Handle state changes of the other sensor."""
        if event.data.get("entity_id") == self._other_sensor_id:
            new_state = event.data.get("new_state")
            if new_state:
                self._state += 1
                self.async_write_ha_state()

