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


NODE_TYPE_THERMOSTAT = NodeType(0x01).set_desc('Thermostat')
NODE_TYPE_GAS_FURNACE = NodeType(0x02).set_desc('Gas Furnace')
NODE_TYPE_AIR_HANDLER = NodeType(0x03).set_desc('Air Handler')
NODE_TYPE_AIR_CONDITIONER = NodeType(0x04).set_desc('Air Conditioner')
NODE_TYPE_HEAT_PUMP = NodeType(0x05).set_desc('Heat Pump')
NODE_TYPE_ELECTRIC_FURNACE = NodeType(0x06).set_desc('Electric Furnace')
NODE_TYPE_PACKAGE_SYSTEM_GAS = NodeType(0x07).set_desc('Package System (Gas)')
NODE_TYPE_PACKAGE_SYSTEM_ELECTRIC = NodeType(0x08).set_desc('Package System (Electric)')
NODE_TYPE_CROSSOVER = NodeType(0x09).set_desc('Crossover(aka OBBI)')
NODE_TYPE_SECONDARY_COMPRESSOR = NodeType(0x0A).set_desc('Secondary Compressor')
NODE_TYPE_AIR_EXCHANGER = NodeType(0x0B).set_desc('Air Exchanger')
NODE_TYPE_UNITARY_CONTROL = NodeType(0x0C).set_desc('Unitary Control')
NODE_TYPE_DEHUMIDIFIER = NodeType(0x0D).set_desc('Dehumidifier')
NODE_TYPE_ELECTRONIC_AIR_CLEANER = NodeType(0x0E).set_desc('Electronic Air Cleaner')
NODE_TYPE_ERV = NodeType(0x0F).set_desc('ERV')
NODE_TYPE_HUMIDIFIER_EVAPORATIVE = NodeType(0x10).set_desc('Humidifier (Evaporative)')
NODE_TYPE_HUMIDIFIER_STEAM = NodeType(0x11).set_desc('Humidifier (Steam)')
NODE_TYPE_HRV = NodeType(0x12).set_desc('HRV')
NODE_TYPE_IAQ_ANALYZER = NodeType(0x13).set_desc('IAQ Analyzer')
NODE_TYPE_MEDIA_AIR_CLEANER = NodeType(0x14).set_desc('Media Air Cleaner')
NODE_TYPE_ZONE_CONTROL = NodeType(0x15).set_desc('Zone Control')
NODE_TYPE_ZONE_USER_INTERFACE = NodeType(0x16).set_desc('Zone User Interface')
NODE_TYPE_BOILER = NodeType(0x17).set_desc('Boiler')
NODE_TYPE_WATER_HEATER_GAS = NodeType(0x18).set_desc('Water Heater (Gas)')
NODE_TYPE_WATER_HEATER_ELECTRIC = NodeType(0x19).set_desc('Water Heater (Electric)')
NODE_TYPE_WATER_HEATER_COMMERCIAL = NodeType(0x1A).set_desc('Water Heater (Commercial)')
NODE_TYPE_POOL_HEATER = NodeType(0x1B).set_desc('Pool Heater')
NODE_TYPE_CEILING_FAN = NodeType(0x1C).set_desc('Ceiling Fan')
NODE_TYPE_GATEWAY = NodeType(0x1D).set_desc('Gateway')
NODE_TYPE_DIAGNOSTIC_DEVICE = NodeType(0x1E).set_desc('Diagnostic Device')
NODE_TYPE_LIGHTING_CONTROL = NodeType(0x1F).set_desc('Lighting Control')
NODE_TYPE_SECURITY_SYSTEM = NodeType(0x20).set_desc('Security System')
NODE_TYPE_UV_LIGHT = NodeType(0x21).set_desc('UV Light')
NODE_TYPE_WEATHER_DATA_DEVICE = NodeType(0x22).set_desc('Weather Data Device')
NODE_TYPE_WHOLE_HOUSE_FAN = NodeType(0x23).set_desc('Whole House Fan')
NODE_TYPE_SOLAR_INVERTER = NodeType(0x24).set_desc('Solar Inverter')
NODE_TYPE_ZONE_DAMPER = NodeType(0x25).set_desc('Zone Damper')
NODE_TYPE_ZONE_TEMPERATURE_CONTROL_ZTC = NodeType(0x26).set_desc('Zone Temperature Control (ZTC)')
NODE_TYPE_TEMPERATURE_SENSOR = NodeType(0x27).set_desc('Temperature Sensor')
NODE_TYPE_OCCUPANCY_SENSOR = NodeType(0x28).set_desc('Occupancy Sensor')
NODE_TYPE_NETWORK_COORDINATOR = NodeType(0xA5).set_desc('Network Coordinator')

NODE_TYPES = [
    NODE_TYPE_THERMOSTAT,
    NODE_TYPE_GAS_FURNACE,
    NODE_TYPE_AIR_HANDLER,
    NODE_TYPE_AIR_CONDITIONER,
    NODE_TYPE_HEAT_PUMP,
    NODE_TYPE_ELECTRIC_FURNACE,
    NODE_TYPE_PACKAGE_SYSTEM_GAS,
    NODE_TYPE_PACKAGE_SYSTEM_ELECTRIC,
    NODE_TYPE_CROSSOVER,
    NODE_TYPE_SECONDARY_COMPRESSOR,
    NODE_TYPE_AIR_EXCHANGER,
    NODE_TYPE_UNITARY_CONTROL,
    NODE_TYPE_DEHUMIDIFIER,
    NODE_TYPE_ELECTRONIC_AIR_CLEANER,
    NODE_TYPE_ERV,
    NODE_TYPE_HUMIDIFIER_EVAPORATIVE,
    NODE_TYPE_HUMIDIFIER_STEAM,
    NODE_TYPE_HRV,
    NODE_TYPE_IAQ_ANALYZER,
    NODE_TYPE_MEDIA_AIR_CLEANER,
    NODE_TYPE_ZONE_CONTROL,
    NODE_TYPE_ZONE_USER_INTERFACE,
    NODE_TYPE_BOILER,
    NODE_TYPE_WATER_HEATER_GAS,
    NODE_TYPE_WATER_HEATER_ELECTRIC,
    NODE_TYPE_WATER_HEATER_COMMERCIAL,
    NODE_TYPE_POOL_HEATER,
    NODE_TYPE_CEILING_FAN,
    NODE_TYPE_GATEWAY,
    NODE_TYPE_DIAGNOSTIC_DEVICE,
    NODE_TYPE_LIGHTING_CONTROL,
    NODE_TYPE_SECURITY_SYSTEM,
    NODE_TYPE_UV_LIGHT,
    NODE_TYPE_WEATHER_DATA_DEVICE,
    NODE_TYPE_WHOLE_HOUSE_FAN,
    NODE_TYPE_SOLAR_INVERTER,
    NODE_TYPE_ZONE_DAMPER,
    NODE_TYPE_ZONE_TEMPERATURE_CONTROL_ZTC,
    NODE_TYPE_TEMPERATURE_SENSOR,
    NODE_TYPE_OCCUPANCY_SENSOR
]