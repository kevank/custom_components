import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import fan,uart
from esphome.const import (
    CONF_OUTPUT_ID,
)

DEPENDENCIES = ['uart']

BUZZER_ENABLE = "buzzer_enable"
REMOTE_ENABLE = "remote_enable"

ifan_ns = cg.esphome_ns.namespace("ifan")
IFan = ifan_ns.class_("IFan", cg.Component, fan.Fan)
IFan04 = ifan_ns.class_('IFan04', cg.Component, uart.UARTDevice)

CONFIG_SCHEMA = fan.FAN_SCHEMA.extend(
    {
        cv.GenerateID(CONF_OUTPUT_ID): cv.declare_id(IFan),
        cv.GenerateID(): cv.declare_id(IFan04),

        cv.Optional(BUZZER_ENABLE, default=True): cv.boolean,
        cv.Optional(REMOTE_ENABLE, default=True): cv.boolean,
    }
).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_OUTPUT_ID])
    cg.add(var.set_buzzer_enable(config[BUZZER_ENABLE]))
    cg.add(var.set_remote_enable(config[REMOTE_ENABLE]))
    if REMOTE_ENABLE in config:
        CONFIG_SCHEMA.extend(uart.UART_DEVICE_SCHEMA)
        await cg.register_component(var, config)
        await uart.register_uart_device(var, config)
    await cg.register_component(var, config)

    await fan.register_fan(var, config)
