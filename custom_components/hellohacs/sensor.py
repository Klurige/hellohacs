from homeassistant.helpers.entity import Entity
from homeassistant.const import EVENT_STATE_CHANGED
from homeassistant.helpers.event import async_track_time_change
from homeassistant.helpers.entity import DeviceInfo
import logging
import datetime
import pytz
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the sensor platform."""
    nordpool_sensor_id = entry.data.get("nordpool_sensor_id")
    device_info = DeviceInfo(
        identifiers={(DOMAIN, entry.entry_id)},
        name="Electricity Price Levels Device",
        manufacturer="Your Manufacturer",
        model="Your Model",
        sw_version="1.0",
    )
    async_add_entities([ExampleSensor(hass, nordpool_sensor_id, device_info), TimeSensor(hass, device_info)])

class ExampleSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass, nordpool_sensor_id, device_info: DeviceInfo):
        self._state = 0
        self._hass = hass
        self._nordpool_sensor_id = nordpool_sensor_id
        self._attr_device_info = device_info
        self._hass.bus.async_listen(EVENT_STATE_CHANGED, self._handle_event)
        _LOGGER.debug("ExampleSensor initialized to listen for %s", nordpool_sensor_id)

    @property
    def name(self):
        return "Example Sensor"

    @property
    def state(self):
        return self._state

    async def _handle_event(self, event):
        """Handle state changes of the other sensor."""
        if event.data.get("entity_id") == self._nordpool_sensor_id:
            new_state = event.data.get("new_state")
            if new_state:
                new_attributes = new_state.attributes

                raw_today = new_attributes.get("raw_today", [])
                raw_tomorrow = new_attributes.get("raw_tomorrow", [])

                _LOGGER.debug("Raw today values: %s", raw_today)
                _LOGGER.debug("Raw tomorrow values: %s", raw_tomorrow)

                self._state += len(raw_today)
                self.async_write_ha_state()
                _LOGGER.debug("ExampleSensor state incremented to %s", self._state)

class TimeSensor(Entity):
    """Representation of a Time Sensor."""

    def __init__(self, hass, device_info: DeviceInfo):
        self._state = None
        self._hass = hass
        self._attr_device_info = device_info
        _LOGGER.debug("TimeSensor initialized")
        # Schedule the first update
        async_track_time_change(hass, self._update_time, second=0)
        # Send the initial value as soon as possible
        hass.loop.create_task(self._send_initial_value())

    @property
    def name(self):
        return "Time Sensor"

    @property
    def state(self):
        return self._state

    async def _send_initial_value(self):
        """Send the initial value with current time but minutes set to 00."""
        local_tz = pytz.timezone(self._hass.config.time_zone)  # Get the time zone from Home Assistant
        now = datetime.datetime.now(local_tz)
        initial_time = now.replace(minute=0, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%S%z")
        self._state = initial_time
        self.async_write_ha_state()

    async def _update_time(self, now):
        """Update the sensor state with the current time."""
        local_tz = pytz.timezone(self._hass.config.time_zone)  # Get the time zone from Home Assistant
        local_time = datetime.datetime.now(local_tz).strftime("%Y-%m-%dT%H:%M:%S%z")
        self._state = local_time
        self.async_write_ha_state()