from homeassistant.helpers.entity import Entity
from homeassistant.const import EVENT_STATE_CHANGED
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the sensor platform."""
    other_sensor_id = entry.data.get("other_sensor_id")
    async_add_entities([ExampleSensor(hass, other_sensor_id)])

class ExampleSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass, other_sensor_id):
        self._state = 0
        self._hass = hass
        self._other_sensor_id = other_sensor_id
        self._hass.bus.async_listen(EVENT_STATE_CHANGED, self._handle_event)
        _LOGGER.debug("ExampleSensor initialized to listen for %s", other_sensor_id)

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
            _LOGGER.debug("Event received for %s: %s", self._other_sensor_id, new_state)
            if new_state:
                self._state += 1
                self.async_write_ha_state()
                _LOGGER.debug("ExampleSensor state incremented to %s", self._state)
