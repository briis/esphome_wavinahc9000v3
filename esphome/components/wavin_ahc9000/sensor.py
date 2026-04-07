import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import (
    UNIT_PERCENT,
    DEVICE_CLASS_BATTERY,
    ICON_BATTERY,
    DEVICE_CLASS_TEMPERATURE,
    UNIT_CELSIUS,
    STATE_CLASS_MEASUREMENT,
)

from . import WavinAHC9000

CONF_PARENT_ID = "wavin_ahc9000_id"
CONF_CHANNEL = "channel"
CONF_TYPE = "type"

# Per-type schema defaults
_SENSOR_DEFAULTS = {
    "battery": sensor.sensor_schema(
        unit_of_measurement=UNIT_PERCENT,
        icon=ICON_BATTERY,
        accuracy_decimals=0,
        device_class=DEVICE_CLASS_BATTERY,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    "temperature": sensor.sensor_schema(
        unit_of_measurement=UNIT_CELSIUS,
        accuracy_decimals=1,
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    "comfort_setpoint": sensor.sensor_schema(
        unit_of_measurement=UNIT_CELSIUS,
        accuracy_decimals=1,
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    "floor_temperature": sensor.sensor_schema(
        unit_of_measurement=UNIT_CELSIUS,
        accuracy_decimals=1,
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    "floor_min_temperature": sensor.sensor_schema(
        unit_of_measurement=UNIT_CELSIUS,
        accuracy_decimals=1,
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    "floor_max_temperature": sensor.sensor_schema(
        unit_of_measurement=UNIT_CELSIUS,
        accuracy_decimals=1,
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
}

def _sensor_schema(config):
    """Validate and apply per-type schema defaults."""
    sensor_type = config[CONF_TYPE]
    schema = _SENSOR_DEFAULTS[sensor_type].extend({
        cv.GenerateID(CONF_PARENT_ID): cv.use_id(WavinAHC9000),
        cv.Required(CONF_CHANNEL): cv.int_range(min=1, max=16),
        cv.Required(CONF_TYPE): cv.one_of(*_SENSOR_DEFAULTS.keys(), lower=True),
    })
    return schema(config)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_PARENT_ID): cv.use_id(WavinAHC9000),
        cv.Required(CONF_CHANNEL): cv.int_range(min=1, max=16),
        cv.Required(CONF_TYPE): cv.one_of(*_SENSOR_DEFAULTS.keys(), lower=True),
    }
).extend(sensor.sensor_schema())

CONFIG_SCHEMA = cv.All(CONFIG_SCHEMA, _sensor_schema)


async def to_code(config):
    hub = await cg.get_variable(config[CONF_PARENT_ID])
    sens = await sensor.new_sensor(config)

    if config[CONF_TYPE] == "battery":
        cg.add(hub.add_channel_battery_sensor(config[CONF_CHANNEL], sens))
    elif config[CONF_TYPE] == "comfort_setpoint":
        cg.add(hub.add_channel_comfort_setpoint_sensor(config[CONF_CHANNEL], sens))
    elif config[CONF_TYPE] == "floor_temperature":
        cg.add(hub.add_channel_floor_temperature_sensor(config[CONF_CHANNEL], sens))
    elif config[CONF_TYPE] == "floor_min_temperature":
        cg.add(hub.add_channel_floor_min_temperature_sensor(config[CONF_CHANNEL], sens))
    elif config[CONF_TYPE] == "floor_max_temperature":
        cg.add(hub.add_channel_floor_max_temperature_sensor(config[CONF_CHANNEL], sens))
    else:
        cg.add(hub.add_channel_temperature_sensor(config[CONF_CHANNEL], sens))

    cg.add(hub.add_active_channel(config[CONF_CHANNEL]))