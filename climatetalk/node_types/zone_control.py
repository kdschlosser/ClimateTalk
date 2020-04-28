# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser

from . import NodeType, Node
from ..commands import (
    HeatSetPointTemperatureModify,
    CoolSetPointTemperatureModify,
    HeatProfileChange,
    CoolProfileChange,
    SystemSwitchModify,
    PermanentSetPointTempHoldModify,
    HoldOverride,
    RealTimeDayOverride,
    RestoreFactoryDefaults,
    TestMode,
    SubsystemInstallationTest,
    AutoPairingRequest1,
    PairingOwnershipRequest1,
    DamperPositionDemand,
    SubsystemBusyStatus,
    DehumidificationDemand,
    HumidificationDemand,
    HeatDemand,
    CoolDemand,
    FanDemand,
    BackUpHeatDemand,
    DefrostDemand,
    AuxHeatDemand
)

NODE_TYPE_ZONE_CONTROL = NodeType(0x15).set_desc('Zone Control')


class ZoneControl(Node):
    node_type = NODE_TYPE_ZONE_CONTROL

