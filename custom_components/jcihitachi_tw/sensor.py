"""JciHitachi integration."""
import logging
import datetime

from homeassistant.components.sensor import SensorEntity, STATE_CLASS_TOTAL_INCREASING, STATE_CLASS_MEASUREMENT
from homeassistant.const import (
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_PM25,
    DEVICE_CLASS_DATE,
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    ENERGY_KILO_WATT_HOUR,
    PERCENTAGE,
)

from . import API, COORDINATOR, MONTHLY_DATA, UPDATED_DATA, JciHitachiEntity

_LOGGER = logging.getLogger(__name__)

ODOR_LEVEL_LOW = "Low"
ODOR_LEVEL_MIDDLE = "Middle"
ODOR_LEVEL_HIGH = "High"


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the sensor platform."""
    
    api = hass.data[API]
    coordinator = hass.data[COORDINATOR]

    for thing in api.things.values():
        if thing.type == "AC":
            async_add_entities(
                [JciHitachiPowerConsumptionSensorEntity(thing, coordinator),
                 JciHitachiMonthlyPowerConsumptionSensorEntity(thing, coordinator),
                 JciHitachiMonthIndicatorSensorEntity(thing, coordinator),
                 ],
                update_before_add=True)
        elif thing.type == "DH":
            async_add_entities(
                [JciHitachiIndoorHumiditySensorEntity(thing, coordinator),
                 JciHitachiOdorLevelSensorEntity(thing, coordinator),
                 JciHitachiPM25SensorEntity(thing, coordinator),
                 JciHitachiPowerConsumptionSensorEntity(thing, coordinator),
                 JciHitachiMonthlyPowerConsumptionSensorEntity(thing, coordinator),
                 JciHitachiMonthIndicatorSensorEntity(thing, coordinator),
                 ],
                update_before_add=True)


async def async_setup_entry(hass, config_entry, async_add_devices):
    """Set up the sensor platform from a config entry."""

    api = hass.data[API]
    coordinator = hass.data[COORDINATOR]

    for thing in api.things.values():
        if thing.type == "AC":
            async_add_devices(
                [JciHitachiPowerConsumptionSensorEntity(thing, coordinator),
                 JciHitachiMonthlyPowerConsumptionSensorEntity(thing, coordinator),
                 JciHitachiMonthIndicatorSensorEntity(thing, coordinator),],
                update_before_add=True)
        elif thing.type == "DH":
            async_add_devices(
                [JciHitachiIndoorHumiditySensorEntity(thing, coordinator),
                 JciHitachiOdorLevelSensorEntity(thing, coordinator),
                 JciHitachiPM25SensorEntity(thing, coordinator),
                 JciHitachiPowerConsumptionSensorEntity(thing, coordinator),
                 JciHitachiMonthlyPowerConsumptionSensorEntity(thing, coordinator),
                 JciHitachiMonthIndicatorSensorEntity(thing, coordinator),],
                update_before_add=True)

class JciHitachiIndoorHumiditySensorEntity(JciHitachiEntity, SensorEntity):
    def __init__(self, thing, coordinator):
        super().__init__(thing, coordinator)

    @property
    def name(self):
        """Return the name of the entity."""
        return f"{self._thing.name} Indoor Humidity"

    @property
    def state(self):
        """Return the indoor humidity."""
        status = self.hass.data[UPDATED_DATA].get(self._thing.name, None)
        if status:
            return status.indoor_humidity
        return None

    @property
    def device_class(self):
        """Return the device class."""
        return DEVICE_CLASS_HUMIDITY

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return PERCENTAGE

    @property
    def unique_id(self):
        return f"{self._thing.gateway_mac_address}_indoor_humidity_sensor"


class JciHitachiPM25SensorEntity(JciHitachiEntity, SensorEntity):
    def __init__(self, thing, coordinator):
        super().__init__(thing, coordinator)

    @property
    def name(self):
        """Return the name of the entity."""
        return f"{self._thing.name} PM2.5"

    @property
    def state(self):
        """Return the PM2.5 value."""
        status = self.hass.data[UPDATED_DATA].get(self._thing.name, None)
        if status:
            return status.pm25_value
        return None

    @property
    def device_class(self):
        """Return the device class."""
        return DEVICE_CLASS_PM25

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return CONCENTRATION_MICROGRAMS_PER_CUBIC_METER

    @property
    def unique_id(self):
        return f"{self._thing.gateway_mac_address}_pm25_sensor"


class JciHitachiOdorLevelSensorEntity(JciHitachiEntity, SensorEntity):
    def __init__(self, thing, coordinator):
        super().__init__(thing, coordinator)

    @property
    def name(self):
        """Return the name of the entity."""
        return f"{self._thing.name} Odor Level"

    @property
    def state(self):
        """Return the odor level."""
        status = self.hass.data[UPDATED_DATA].get(self._thing.name, None)
        if status:
            if status.odor_level == "low":
                return ODOR_LEVEL_LOW
            elif status.odor_level == "middle":
                return ODOR_LEVEL_MIDDLE
            elif status.odor_level == "high":
                return ODOR_LEVEL_HIGH
        return None

    @property
    def unique_id(self):
        return f"{self._thing.gateway_mac_address}_odor_level_sensor"


class JciHitachiPowerConsumptionSensorEntity(JciHitachiEntity, SensorEntity):
    def __init__(self, thing, coordinator):
        super().__init__(thing, coordinator)

    @property
    def name(self):
        """Return the name of the entity."""
        return f"{self._thing.name} Power Consumption"

    @property
    def state(self):
        """Return the power consumption in KW/H"""
        status = self.hass.data[UPDATED_DATA].get(self._thing.name, None)
        if status:
            return status.power_kwh
        return None

    @property
    def device_class(self):
        """Return the device class."""
        return DEVICE_CLASS_ENERGY

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return ENERGY_KILO_WATT_HOUR

    @property
    def unique_id(self):
        return f"{self._thing.gateway_mac_address}_power_consumption_sensor"

    @property
    def state_class(self):
        return STATE_CLASS_TOTAL_INCREASING

class JciHitachiMonthlyPowerConsumptionSensorEntity(JciHitachiEntity, SensorEntity):
    def __init__(self, thing, coordinator):
        super().__init__(thing, coordinator)

    @property
    def name(self):
        """Return the name of the entity."""
        return f"{self._thing.name} Monthly Power Consumption"

    @property
    def state(self):
        """Return the monthly power consumption in KW/H"""
        monthly_data = self.hass.data[MONTHLY_DATA]
        if monthly_data:
            return monthly_data[0]["PowerConsumption_Sum"] / 10
        return -1

    @property
    def device_class(self):
        """Return the device class."""
        return DEVICE_CLASS_ENERGY

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return ENERGY_KILO_WATT_HOUR

    @property
    def unique_id(self):
        return f"{self._thing.gateway_mac_address}_monthly_power_consumption_sensor"
    
    @property
    def state_class(self):
        return STATE_CLASS_MEASUREMENT

class JciHitachiMonthIndicatorSensorEntity(JciHitachiEntity, SensorEntity):
    def __init__(self, thing, coordinator):
        super().__init__(thing, coordinator)

    @property
    def name(self):
        """Return the name of the entity."""
        return f"{self._thing.name} Month Indicator"

    @property
    def state(self):
        """Return the month in yyyy-mm format."""
        value = self.native_value
        if value is not None:
            return self.native_value.strftime("%Y-%m")
        return None
        
    @property
    def native_value(self):
        """Return the month in datetime.date object."""
        monthly_data = self.hass.data[MONTHLY_DATA]
        if monthly_data:
            return datetime.date.fromtimestamp(monthly_data[0]["Timestamp"] / 1000)
        return None

    @property
    def device_class(self):
        """Return the device class."""
        return DEVICE_CLASS_DATE

    @property
    def unique_id(self):
        return f"{self._thing.gateway_mac_address}_month_indicator_sensor"