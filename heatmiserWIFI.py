"""
Support for the PRT Heatmiser themostats using the V3 protocol.
For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/climate.heatmiser/
"""
import logging
from . import heatmiser_wifi

import voluptuous as vol

from homeassistant.components.climate import (
    ClimateDevice, PLATFORM_SCHEMA, SUPPORT_TARGET_TEMPERATURE, ATTR_MIN_TEMP)
from homeassistant.const import (
    TEMP_CELSIUS, ATTR_TEMPERATURE, CONF_PORT, CONF_NAME, CONF_ID, CONF_PIN)
import homeassistant.helpers.config_validation as cv

#REQUIREMENTS = ['heatmiser_wifi']

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "Heatmiser WIFI"

CONF_IPADDRESS = 'ipaddress'
#CONF_TSTATS = 'tstats'

#TSTATS_SCHEMA = vol.Schema({
#    vol.Required(CONF_ID): cv.string,
#    vol.Required(CONF_NAME): cv.string,
#})



PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_IPADDRESS): cv.string,
    vol.Required(CONF_PORT): cv.port,
	vol.Required(CONF_PIN): cv.positive_int,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
#    vol.Required(CONF_TSTATS, default={}):
#        vol.Schema({cv.string: TSTATS_SCHEMA}),
})

# pylint: disable=unused-variable
def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the heatmiser thermostat."""
#    from heatmaster_wifi import heatmaster_wifi
    

    ipaddress = config.get(CONF_IPADDRESS)	
    port = str(config.get(CONF_PORT))
    pin = str(config.get(CONF_PIN))
    name = str(config.get(CONF_NAME))
#    tstats = config.get(CONF_TSTATS)
	
#	add_devices(heatmiser = Heatmiser(ipaddress, port, pin))

#    serport = connection.connection(ipaddress, port)
#    serport.open()

#    for tstat in tstats.values():
    add_devices([HeatmiserV3Thermostat(heatmiser_wifi, port, ipaddress, pin, name)])
#    return


class HeatmiserV3Thermostat(ClimateDevice):
    """Representation of a HeatmiserV3 thermostat."""

    def __init__(self, heatmiser_wifi, port, ipaddress, pin, name):
        """Initialize the thermostat."""
        self.heatmiser = heatmiser_wifi.Heatmiser(ipaddress, int(port), pin)
        self.device = 1
        self.port = port
        self.pin = pin
        self._current_temperature = None
        self._name = name
        self._id = 1
        self.dcb = None
        self.update()
        self._target_temperature = int(self.dcb.get('set_room_temp'))
        self._min_temp = 5

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_TARGET_TEMPERATURE

    @property
    def name(self):
        """Return the name of the thermostat, if any."""
        return self._name

    @property
    def temperature_unit(self):
        """Return the unit of measurement which this thermostat uses."""
        return TEMP_CELSIUS
    
    @property
    def min_temp(self):
        """Return the minimum temperature."""
        # pylint: disable=no-member
        if self._min_temp:
            return self._min_temp

        # get default temp from super class
        return ClimateDevice.min_temp.fget(self)

    @property
    def current_temperature(self):
        """Return the current temperature."""
        if self.dcb is not None:
            self._current_temperature = self.dcb.get('floor_temp')
        else:
            self._current_temperature = None
        return self._current_temperature

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._target_temperature

    def set_temperature(self, **kwargs):
        """Set new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return
        self.heatmiser.connect()
        self.heatmiser.set_value('set_room_temp', temperature)
        self._target_temperature = temperature

    def update(self):
        """Get the latest data."""
        self.heatmiser.connect()
        self.dcb = self.heatmiser.get_info()
        self.heatmiser.disconnect()
		
	