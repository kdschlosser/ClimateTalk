# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser


class NodeType(int):
    def __init__(self, value):
        try:
            int.__init__(self, value)
        except TypeError:
            int.__init__(self)

        self._desc = ''

    def set_desc(self, desc):
        self._desc = desc
        return self

    def __str__(self):
        return self._desc


THERMOSTAT = NodeType(0x01).set_desc('Thermostat')
GAS_FURNACE = NodeType(0x02).set_desc('Gas Furnace')
AIR_HANDLER = NodeType(0x03).set_desc('Air Handler')
AIR_CONDITIONER = NodeType(0x04).set_desc('Air Conditioner')
HEAT_PUMP = NodeType(0x05).set_desc('Heat Pump')
ELECTRIC_FURNACE = NodeType(0x06).set_desc('Electric Furnace')
PACKAGE_SYSTEM_GAS = NodeType(0x07).set_desc('Package System (Gas)')
PACKAGE_SYSTEM_ELECTRIC = NodeType(0x08).set_desc('Package System (Electric)')
CROSSOVERAKA_OBBI = NodeType(0x09).set_desc('Crossover(aka OBBI)')
SECONDARY_COMPRESSOR = NodeType(0x0A).set_desc('Secondary Compressor')
AIR_EXCHANGER = NodeType(0x0B).set_desc('Air Exchanger')
UNITARY_CONTROL = NodeType(0x0C).set_desc('Unitary Control')
DEHUMIDIFIER = NodeType(0x0D).set_desc('Dehumidifier')
ELECTRONIC_AIR_CLEANER = NodeType(0x0E).set_desc('Electronic Air Cleaner')
ERV = NodeType(0x0F).set_desc('ERV')
HUMIDIFIER_EVAPORATIVE = NodeType(0x10).set_desc('Humidifier (Evaporative)')
HUMIDIFIER_STEAM = NodeType(0x11).set_desc('Humidifier (Steam)')
HRV = NodeType(0x12).set_desc('HRV')
IAQ_ANALYZER = NodeType(0x13).set_desc('IAQ Analyzer')
MEDIA_AIR_CLEANER = NodeType(0x14).set_desc('Media Air Cleaner')
ZONE_CONTROL = NodeType(0x15).set_desc('Zone Control')
ZONE_USER_INTERFACE = NodeType(0x16).set_desc('Zone User Interface')
BOILER = NodeType(0x17).set_desc('Boiler')
WATER_HEATER_GAS = NodeType(0x18).set_desc('Water Heater (Gas)')
WATER_HEATER_ELECTRIC = NodeType(0x19).set_desc('Water Heater (Electric)')
WATER_HEATER_COMMERCIAL = NodeType(0x1A).set_desc('Water Heater (Commercial)')
POOL_HEATER = NodeType(0x1B).set_desc('Pool Heater')
CEILING_FAN = NodeType(0x1C).set_desc('Ceiling Fan')
GATEWAY = NodeType(0x1D).set_desc('Gateway')
DIAGNOSTIC_DEVICE = NodeType(0x1E).set_desc('Diagnostic Device')
LIGHTING_CONTROL = NodeType(0x1F).set_desc('Lighting Control')
SECURITY_SYSTEM = NodeType(0x20).set_desc('Security System')
UV_LIGHT = NodeType(0x21).set_desc('UV Light')
WEATHER_DATA_DEVICE = NodeType(0x22).set_desc('Weather Data Device')
WHOLE_HOUSE_FAN = NodeType(0x23).set_desc('Whole House Fan')
SOLAR_INVERTER = NodeType(0x24).set_desc('Solar Inverter')
ZONE_DAMPER = NodeType(0x25).set_desc('Zone Damper')
ZONE_TEMPERATURE_CONTROL_ZTC = NodeType(0x26).set_desc('Zone Temperature Control (ZTC)')
TEMPERATURE_SENSOR = NodeType(0x27).set_desc('Temperature Sensor')
OCCUPANCY_SENSOR = NodeType(0x28).set_desc('Occupancy Sensor')
NETWORK_COORDINATOR = NodeType(0xA5).set_desc('Network Coordinator')

NODE_TYPES = [
    THERMOSTAT,
    GAS_FURNACE,
    AIR_HANDLER,
    AIR_CONDITIONER,
    HEAT_PUMP,
    ELECTRIC_FURNACE,
    PACKAGE_SYSTEM_GAS,
    PACKAGE_SYSTEM_ELECTRIC,
    CROSSOVERAKA_OBBI,
    SECONDARY_COMPRESSOR,
    AIR_EXCHANGER,
    UNITARY_CONTROL,
    DEHUMIDIFIER,
    ELECTRONIC_AIR_CLEANER,
    ERV,
    HUMIDIFIER_EVAPORATIVE,
    HUMIDIFIER_STEAM,
    HRV,
    IAQ_ANALYZER,
    MEDIA_AIR_CLEANER,
    ZONE_CONTROL,
    ZONE_USER_INTERFACE,
    BOILER,
    WATER_HEATER_GAS,
    WATER_HEATER_ELECTRIC,
    WATER_HEATER_COMMERCIAL,
    POOL_HEATER,
    CEILING_FAN,
    GATEWAY,
    DIAGNOSTIC_DEVICE,
    LIGHTING_CONTROL,
    SECURITY_SYSTEM,
    UV_LIGHT,
    WEATHER_DATA_DEVICE,
    WHOLE_HOUSE_FAN,
    SOLAR_INVERTER,
    ZONE_DAMPER,
    ZONE_TEMPERATURE_CONTROL_ZTC,
    TEMPERATURE_SENSOR,
    OCCUPANCY_SENSOR
]