# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

import six

'''
    AdvanceRealTimeDayOverride,
    AutoPairingRequest1,
    AutoPairingRequest2,
    AuxHeatDemand,
    BackUpHeatDemand,
    BeeperEnable,
    ChangeFilterTimeRemaining,
    ChangeHumidifierPadMaintTimerall,
    ChangeUvLightMaintenanceTimer,
    ClearCompressorRunTime,
    ComfortModeModification,
    ComfortRecoveryModify,
    CommandPacketBase,
    CommunicationsReceiverOnOff,
    CompressorLockout,
    ContinuousDisplayLight,
    ControlCommandRefreshTimer,
    CoolDemand,
    CoolProfileChange,
    CoolSetPointTemperatureModify,
    CustomMessageAreaDisplayData,
    DamperClosurePositionDemand,
    DefrostDemand,
    DehumidificationDemand,
    DehumidificationSetPointModify,
    DemandBase,
    FahrenheitCelsiusDisplay,
    FanDemand,
    FanKeySelection,
    ForcePhoneNumberDisplay,
    HeatDemand,
    HeatProfileChange,
    HeatSetPointTemperatureModify,
    HighAlarmLimitChange,
    HighOutdoorAlarmLimitChange,
    HoldRelease,
    HumDehumConfig,
    HumidificationDemand,
    HumidificationSetPointModify,
    HvacHoldOverride,
    KeypadLockout,
    LimitedHeatAndCoolRange,
    LowAlarmLimitChange,
    LowOutdoorAlarmLimitChange,
    PairingOwnershipRequest1,
    PairingOwnershipRequest2,
    PermanentSetPointTempHoldModify,
    ProgramIntervalTypeModification,
    PublishPrice,
    RealTimeDayOverride,
    ResetMicro,
    RestoreFactoryDefaults,
    ReversingValveConfig,
    RunStopMotor,
    SetAirflowDemand,
    SetAirflowLimit,
    SetBlowerCoefficient1,
    SetBlowerCoefficient10,
    SetBlowerCoefficient2,
    SetBlowerCoefficient3,
    SetBlowerCoefficient4,
    SetBlowerCoefficient5,
    SetBlowerCoefficient6,
    SetBlowerCoefficient7,
    SetBlowerCoefficient8,
    SetBlowerCoefficient9,
    SetBlowerCoefficientBase,
    SetBlowerIdentification0,
    SetBlowerIdentification1,
    SetBlowerIdentification2,
    SetBlowerIdentification3,
    SetBlowerIdentification4,
    SetBlowerIdentification5,
    SetBlowerIdentificationBase,
    SetControlMode,
    SetDemandRampRate,
    SetDemandRampTime,
    SetDeviceTemperatureLimit,
    SetInducerRampRate,
    SetMotorDirection,
    SetMotorPositionDemand,
    SetMotorSpeed,
    SetMotorTorque,
    SetMotorTorquePercent,
    SetPointTempAndTemporaryHold,
    SetPointTempTimeHold,
    SetPowerOutputLimit,
    SetSpeedLimit,
    SetTorqueLimit,
    StopMotorByBraking,
    SubsystemBusyStatus,
    SubsystemInstallationTest,
    SystemSwitchModify,
    TempDisplayAdjFactorChange,
    TestMode,
    VacationMode,
    WaterHeaterModify,
'''


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


class NodeMeta(type):
    instances = {}

    def __call__(cls, network, address, subnet, mac_address, session_id, node_type=None):
        if cls == Node:
            for n_type in NODE_TYPES:
                if n_type.node_type == node_type:
                    break
            else:
                raise RuntimeError(str(node_type))

            return n_type(network, address, subnet, mac_address, session_id)

        if (address, subnet) not in NodeMeta.instances:
            NodeMeta.instances[(address, subnet)] = (
                super(NodeMeta, cls).__call__(network, address, subnet, mac_address, session_id)
            )

        return NodeMeta.instances[(address, subnet)]


@six.add_metaclass(NodeMeta)
class Node(object):

    def __init__(self, network, address, subnet, mac_address, session_id, _=None):
        self.network = network
        self.address = address
        self.subnet = subnet
        self.mac_address = mac_address
        self.session_id = session_id


from . import thermostat  # NOQA
from . import air_handler  # NOQA
from . import air_conditioner  # NOQA
from . import heat_pump  # NOQA
from . import furnace_electric  # NOQA
from . import furnace_gas  # NOQA
from . import package_system_gas  # NOQA
from . import package_system_electric  # NOQA
from . import crossover  # NOQA
from . import secondary_compressor  # NOQA
from . import air_exchanger  # NOQA
from . import unitary_control  # NOQA
from . import dehumidifier  # NOQA
from . import electronic_air_cleaner  # NOQA
from . import erv  # NOQA
from . import humidifier_evaporative  # NOQA
from . import humidifier_steam  # NOQA
from . import hrv  # NOQA
from . import iaq_analyzer  # NOQA
from . import media_air_cleaner  # NOQA
from . import zone_control  # NOQA
from . import zone_user_interface  # NOQA
from . import boiler  # NOQA
from . import water_heater_gas  # NOQA
from . import water_heater_electric  # NOQA
from . import water_heater_commercial  # NOQA
from . import pool_heater  # NOQA
from . import ceiling_fan  # NOQA
from . import gateway  # NOQA
from . import diagnostic_device  # NOQA
from . import lighting_control  # NOQA
from . import security_system  # NOQA
from . import uv_light  # NOQA
from . import weather_data_device  # NOQA
from . import whole_house_fan  # NOQA
from . import solar_inverter  # NOQA
from . import zone_damper  # NOQA
from . import zone_temperature_control  # NOQA
from . import temperature_sensor  # NOQA
from . import occupancy_sensor  # NOQA


NODE_TYPES = (
    thermostat.Thermostat,
    air_handler.AirHandler,
    air_conditioner.AirConditioner,
    heat_pump.HeatPump,
    furnace_electric.FurnaceElectric,
    furnace_gas.FurnaceGas,
    package_system_gas.PackageSystemGas,
    package_system_electric.PackageSystemElectric,
    crossover.Crossover,
    secondary_compressor.SecondaryCompressor,
    air_exchanger.AirExchanger,
    unitary_control.UnitaryControl,
    dehumidifier.Dehumidifier,
    electronic_air_cleaner.ElectronicAirCleaner,
    erv.ERV,
    humidifier_evaporative.HumidifierEvaporative,
    humidifier_steam.HumidifierSteam,
    hrv.HRV,
    iaq_analyzer.IAQAnalyzer,
    media_air_cleaner.MediaAirCleaner,
    zone_control.ZoneControl,
    zone_user_interface.ZoneUserInterface,
    boiler.Boiler,
    water_heater_gas.WaterHeaterGas,
    water_heater_electric.WaterHeaterElectric,
    water_heater_commercial.WaterHeaterCommercial,
    pool_heater.PoolHeater,
    ceiling_fan.CeilingFan,
    gateway.Gateway,
    diagnostic_device.DiagnosticDevice,
    lighting_control.LightingControl,
    security_system.SecuritySystem,
    uv_light.UVLight,
    weather_data_device.WeatherDataDevice,
    whole_house_fan.WholeHouseFan,
    solar_inverter.SolarInverter,
    zone_damper.ZoneDamper,
    zone_temperature_control.ZoneTemperatureControl,
    temperature_sensor.TemperatureSensor,
    occupancy_sensor.OccupancySensor
)
