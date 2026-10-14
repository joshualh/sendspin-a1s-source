"""Expose the Sendspin pairing token as an opt-in diagnostic text sensor."""

import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text_sensor
from esphome.const import ENTITY_CATEGORY_DIAGNOSTIC

from . import CONF_SENDSPIN_ID, SendspinHub, sendspin_ns

DEPENDENCIES = ["sendspin"]

CONF_PAIRING_TOKEN = "pairing_token"

SendspinPairingTokenTextSensor = sendspin_ns.class_(
    "SendspinPairingTokenTextSensor",
    text_sensor.TextSensor,
    cg.PollingComponent,
    cg.Parented.template(SendspinHub),
)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_SENDSPIN_ID): cv.use_id(SendspinHub),
        cv.Optional(CONF_PAIRING_TOKEN): text_sensor.text_sensor_schema(
            SendspinPairingTokenTextSensor,
            entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
        ).extend(cv.polling_component_schema("5s")),
    }
)


async def to_code(config):
    if conf := config.get(CONF_PAIRING_TOKEN):
        var = await text_sensor.new_text_sensor(conf)
        await cg.register_component(var, conf)
        await cg.register_parented(var, config[CONF_SENDSPIN_ID])
