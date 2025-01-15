from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN

class ExampleConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Example config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate user input here
            if self._validate_input(user_input):
                return self.async_create_entry(title="Example Integration", data=user_input)
            else:
                errors["base"] = "invalid_input"

        return self.async_show_form(
            step_id="user",
            data_schema=self._get_schema(),
            errors=errors
        )

    @staticmethod
    @callback
    def _get_schema():
        """Return the schema for the user input."""
        import voluptuous as vol
        return vol.Schema({
            vol.Required("username"): str,
            vol.Required("password"): str,
        })

    def _validate_input(self, data):
        """Validate the user input."""
        # Add your validation logic here
        return True
