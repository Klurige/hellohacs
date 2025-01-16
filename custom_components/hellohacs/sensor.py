from homeassistant.helpers.entity import Entity
from homeassistant.const import EVENT_STATE_CHANGED
from homeassistant.helpers.event import async_track_time_change
import logging
import datetime
import pytz

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the sensor platform."""
    other_sensor_id = entry.data.get("other_sensor_id")
    async_add_entities([ExampleSensor(hass, other_sensor_id), TimeSensor(hass)])

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

class TimeSensor(Entity):
    """Representation of a Time Sensor."""

    def __init__(self, hass):
        self._state = None
        self._hass = hass
        _LOGGER.debug("TimeSensor initialized")
        # Schedule the first update
        async_track_time_change(hass, self._update_time, second=0)

    @property
    def name(self):
        return "Time Sensor"

    @property
    def state(self):
        return self._state

    async def _update_time(self, now):
        """Update the sensor state with the current time."""
        local_tz = pytz.timezone(self._hass.config.time_zone)  # Get the time zone from Home Assistant
        local_time = datetime.datetime.now(local_tz).strftime("%Y-%m-%dT%H:%M:%S%z")
        self._state = local_time
        self.async_write_ha_state()
