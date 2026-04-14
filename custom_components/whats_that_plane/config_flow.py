import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN

DISTANCE_IMPERIAL = "imperial (miles (mi))"
DISTANCE_METRIC = "metric (kilometres (km))"
ALTITUDE_IMPERIAL = "imperial (feet (ft))"
ALTITUDE_METRIC = "metric (metres (m))"
SPEED_IMPERIAL = "imperial (miles per hour (mph))"
SPEED_METRIC = "metric (kilometres per hour (km/h))"

class WhatsThatPlaneConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            location_name = user_input.get("location_name", "").strip()
            title = "Visible Flights"
            if location_name:
                title = f"Visible Flights ({location_name})"
            return self.async_create_entry(title=title, data=user_input)

        default_latitude = self.hass.config.latitude
        default_longitude = self.hass.config.longitude

        data_schema = vol.Schema({
            vol.Optional("location_name"): str,
            vol.Required("latitude", default=default_latitude): vol.All(vol.Coerce(float), vol.Range(min=-90, max=90)),
            vol.Required("longitude", default=default_longitude): vol.All(vol.Coerce(float), vol.Range(min=-180, max=180)),
            vol.Required("radius_km", default=5): vol.All(vol.Coerce(int), vol.Range(min=1, max=500)),
            vol.Required("facing_direction", default=0): vol.All(vol.Coerce(int), vol.Range(min=0, max=360)),
            vol.Required("fov_cone", default=90): vol.All(vol.Coerce(int), vol.Range(min=1, max=360)),
            vol.Required("update_interval", default=10): vol.All(vol.Coerce(int), vol.Range(min=10)),
            vol.Optional("filter_flight_altitude_ft_minimum", default=0): vol.All(vol.Coerce(int), vol.Range(min=0)),
            vol.Optional("filter_flight_altitude_ft_maximum", default=60000): vol.All(vol.Coerce(int), vol.Range(min=0)),
            vol.Optional("hold_flight_data_seconds", default=0): vol.All(vol.Coerce(int), vol.Range(min=0)),
            vol.Optional("historic_flights_max_count", default=0): vol.All(vol.Coerce(int), vol.Range(min=0)),
            vol.Optional("landing_detection_enabled", default=False): bool,
            vol.Optional("runway_heading", default=0): vol.All(vol.Coerce(int), vol.Range(min=0, max=360)),
            vol.Optional("approach_cone_width", default=30): vol.All(vol.Coerce(int), vol.Range(min=1, max=180)),
            vol.Optional("landing_altitude_max_ft", default=5000): vol.All(vol.Coerce(int), vol.Range(min=100, max=60000)),
            vol.Optional("landing_speed_max_kts", default=200): vol.All(vol.Coerce(int), vol.Range(min=0, max=999)),
            vol.Optional("distance_units", default=DISTANCE_IMPERIAL): vol.In([DISTANCE_METRIC, DISTANCE_IMPERIAL]),
            vol.Optional("altitude_units", default=ALTITUDE_IMPERIAL): vol.In([ALTITUDE_METRIC, ALTITUDE_IMPERIAL]),
            vol.Optional("speed_units", default=SPEED_IMPERIAL): vol.In([SPEED_METRIC, SPEED_IMPERIAL]),
        })
        return self.async_show_form(step_id="user", data_schema=data_schema)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return WhatsThatPlaneOptionsFlow()


class WhatsThatPlaneOptionsFlow(config_entries.OptionsFlow):
    async def async_step_init(self, user_input=None):
        if user_input is not None:
            new_options = {**self.config_entry.options, **user_input}

            location_name = new_options.get("location_name", "").strip()
            title = "Visible Flights"
            if location_name:
                title = f"Visible Flights ({location_name})"
            
            self.hass.config_entries.async_update_entry(
                self.config_entry, title=title
            )
            return self.async_create_entry(title="", data=new_options)

        current_config = {**self.config_entry.data, **self.config_entry.options}
        options_schema = vol.Schema({
            vol.Optional("location_name", default=current_config.get("location_name", "")): str,
            vol.Required("latitude", default=current_config.get("latitude")): vol.All(vol.Coerce(float), vol.Range(min=-90, max=90)),
            vol.Required("longitude", default=current_config.get("longitude")): vol.All(vol.Coerce(float), vol.Range(min=-180, max=180)),
            vol.Required("radius_km", default=current_config.get("radius_km")): vol.All(vol.Coerce(int), vol.Range(min=1, max=500)),
            vol.Required("facing_direction", default=current_config.get("facing_direction")): vol.All(vol.Coerce(int), vol.Range(min=0, max=360)),
            vol.Required("fov_cone", default=current_config.get("fov_cone")): vol.All(vol.Coerce(int), vol.Range(min=1, max=360)),
            vol.Required("update_interval", default=current_config.get("update_interval")): vol.All(vol.Coerce(int), vol.Range(min=10)),
            vol.Optional("filter_flight_altitude_ft_minimum", default=current_config.get("filter_flight_altitude_ft_minimum", 0)): vol.All(vol.Coerce(int), vol.Range(min=0)),
            vol.Optional("filter_flight_altitude_ft_maximum", default=current_config.get("filter_flight_altitude_ft_maximum", 60000)): vol.All(vol.Coerce(int), vol.Range(min=0)),
            vol.Optional("hold_flight_data_seconds", default=current_config.get("hold_flight_data_seconds", 0)): vol.All(vol.Coerce(int), vol.Range(min=0)),
            vol.Optional("historic_flights_max_count", default=current_config.get("historic_flights_max_count", 0)): vol.All(vol.Coerce(int), vol.Range(min=0)),
            vol.Optional("landing_detection_enabled", default=current_config.get("landing_detection_enabled", False)): bool,
            vol.Optional("runway_heading", default=current_config.get("runway_heading", 0)): vol.All(vol.Coerce(int), vol.Range(min=0, max=360)),
            vol.Optional("approach_cone_width", default=current_config.get("approach_cone_width", 30)): vol.All(vol.Coerce(int), vol.Range(min=1, max=180)),
            vol.Optional("landing_altitude_max_ft", default=current_config.get("landing_altitude_max_ft", 5000)): vol.All(vol.Coerce(int), vol.Range(min=100, max=60000)),
            vol.Optional("landing_speed_max_kts", default=current_config.get("landing_speed_max_kts", 200)): vol.All(vol.Coerce(int), vol.Range(min=0, max=999)),
            vol.Optional("distance_units", default=current_config.get("distance_units", DISTANCE_IMPERIAL)): vol.In([DISTANCE_METRIC, DISTANCE_IMPERIAL]),
            vol.Optional("altitude_units", default=current_config.get("altitude_units", ALTITUDE_IMPERIAL)): vol.In([ALTITUDE_METRIC, ALTITUDE_IMPERIAL]),
            vol.Optional("speed_units", default=current_config.get("speed_units", SPEED_IMPERIAL)): vol.In([SPEED_METRIC, SPEED_IMPERIAL]),
        })
        return self.async_show_form(step_id="init", data_schema=options_schema)