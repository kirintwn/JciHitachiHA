"""JciHitachi integration."""
import logging

from homeassistant.components.number import NumberEntity

from . import API, COORDINATOR, MONTHLY_DATA, JciHitachiEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the number platform."""
    
    api = hass.data[API]
    coordinator = hass.data[COORDINATOR]

    for thing in api.things.values():
        async_add_entities(
            [
                JciHitachiMonthlyDataSelectorNumberEntity(thing, coordinator)
            ],
            update_before_add=True
        )


async def async_setup_entry(hass, config_entry, async_add_devices):
    """Set up the number platform from a config entry."""

    api = hass.data[API]
    coordinator = hass.data[COORDINATOR]

    for thing in api.things.values():
        async_add_devices(
            [
                JciHitachiMonthlyDataSelectorNumberEntity(thing, coordinator)
            ],
            update_before_add=True
        )


class JciHitachiMonthlyDataSelectorNumberEntity(JciHitachiEntity, NumberEntity):
    def __init__(self, thing, coordinator):
        super().__init__(thing, coordinator)
        self._value = 0

    @property
    def name(self):
        """Return the name of the entity."""
        return f"{self._thing.name} Month Selector"
    
    @property
    def value(self):
        """Return the value of the entity."""
        return self._value

    @property
    def min_value(self):
        """Return the minimum month."""
        return 0

    @property
    def max_value(self):
        """Return the maximum month."""
        return 12

    @property
    def unique_id(self):
        return f"{self._thing.gateway_mac_address}_monthly_data_selector_number"

    def set_value(self, value):
        """Set new month."""
        _LOGGER.debug(f"Set {self.name} value to {value}")
        self._value = value

        api = self.hass.data[API]
        self.hass.data[MONTHLY_DATA] = api.get_monthly_data(int(self._value), self._thing.name)
        self.update()