# ClimateTalk
Python binding to the ClimateTalk Protocol (used in HVAC systems)

This is a work in progress.


You will need some hardware in order to use this library. 
You will need an RS485 to IP device, this device can be made with an 
ESP32 development board and a MAX RS485 development board.
I would recommend purchasing a MAX development board that is 
RS485 to TTL so you will not have to worry about changing 
from receive mode to send mode.

I will be adding a MicroPython boot script that you will be able to 
upload into the ESP32. I will also provide instructions on how to 
flash MicroPython and what is going to be needed to do that.

I am in the initial stages of development and nothing has been 
tested at this point. I should have a working receiving end 
within the next 2-3 days, sending is going to take a bit longer.


This library is only going to work for home/building mechanical 
that supports the ClimateTalk protocol. The device MUST be a 
"communicating device" If it is not then it is not going to support 
the ClimateTalk protocol.

Older Rheem/Ruud units that have Comfort Control 2 are using the ClimateTalk
protocol. I believe their EcoNet protocol is based on the ClimateTalk protocol
and would probably not be to difficult to reverse engineer once this is working.

The purpose to this library is so you can get control of the mechanical
devices in your home without having to rely on an internet connntion or
having to rely on the API of a manufacturers website. This is a direct 
connection to the device, so no "middle man".

This is a list of possible devices that may support the ClimateTalk protocol

* Thermostat
* Gas Furnace
* Air Handler
* Air Conditioner
* Heat Pump
* Electric Furnace
* Package System (Gas)
* Package System (Electric)
* Crossover(aka OBBI)
* Secondary Compressor
* Air Exchanger
* Unitary Control
* Dehumidifier
* Electronic Air Cleaner
* ERV
* Humidifier (Evaporative)
* Humidifier (Steam)
* HRV
* IAQ Analyzer
* Media Air Cleaner
* Zone Control
* Zone User Interface
* Boiler
* Water Heater (Gas)
* Water Heater (Electric)
* Water Heater (Commercial)
* Pool Heater
* Ceiling Fan
* Gateway
* Diagnostic Device
* Lighting Control
* Security System
* UV Light
* Weather Data Device
* Whole House Fan
* Solar Inverter
* Zone Damper
* Zone Temperature Control (ZTC)
* Temperature Sensor
* Occupancy Sensor
