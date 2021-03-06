
# Message Received with Correct CRC
ACK1 = 0x06  # Valid command - Only sent for control commands from master
ACK2 = 0x0A  # Undesired Parameter Sent
ACK3 = 0x0D  # Minimum Parameters Not Complete

NAK1 = 0x15  # Message Received with Incorrect CRC
NAK2 = 0x1B  # Invalid message for that specific application implementation


LWP_NODE_TYPE_BLOWER_MOTOR_1 = 0x0A
LWP_NODE_TYPE_BLOWER_MOTOR_2 = 0x0B
LWP_NODE_TYPE_BLOWER_MOTOR_3 = 0x0C
LWP_NODE_TYPE_BLOWER_MOTOR_4 = 0x0D
LWP_NODE_TYPE_BLOWER_MOTOR_5 = 0x0E
LWP_NODE_TYPE_BLOWER_MOTOR_6 = 0x0F
LWP_NODE_TYPE_BLOWER_MOTOR_7 = 0x10
LWP_NODE_TYPE_BLOWER_MOTOR_8 = 0x11
LWP_NODE_TYPE_BLOWER_MOTOR_9 = 0x12
LWP_NODE_TYPE_BLOWER_MOTOR_10 = 0x13

LWP_NODE_TYPE_INDUCER_MOTOR_1 = 0x14
LWP_NODE_TYPE_INDUCER_MOTOR_2 = 0x15
LWP_NODE_TYPE_INDUCER_MOTOR_3 = 0x16
LWP_NODE_TYPE_INDUCER_MOTOR_4 = 0x17
LWP_NODE_TYPE_INDUCER_MOTOR_5 = 0x18
LWP_NODE_TYPE_INDUCER_MOTOR_6 = 0x19
LWP_NODE_TYPE_INDUCER_MOTOR_7 = 0x1A
LWP_NODE_TYPE_INDUCER_MOTOR_8 = 0x1B
LWP_NODE_TYPE_INDUCER_MOTOR_9 = 0x1C
LWP_NODE_TYPE_INDUCER_MOTOR_10 = 0x1D

LWP_NODE_TYPE_OUTDOOR_MOTOR_1 = 0x1E
LWP_NODE_TYPE_OUTDOOR_MOTOR_2 = 0x1F
LWP_NODE_TYPE_OUTDOOR_MOTOR_3 = 0x20
LWP_NODE_TYPE_OUTDOOR_MOTOR_4 = 0x21
LWP_NODE_TYPE_OUTDOOR_MOTOR_5 = 0x22
LWP_NODE_TYPE_OUTDOOR_MOTOR_6 = 0x23
LWP_NODE_TYPE_OUTDOOR_MOTOR_7 = 0x24
LWP_NODE_TYPE_OUTDOOR_MOTOR_8 = 0x25
LWP_NODE_TYPE_OUTDOOR_MOTOR_9 = 0x26
LWP_NODE_TYPE_OUTDOOR_MOTOR_10 = 0x27

LWP_NODE_TYPE_GAS_STEPPER_MOTOR_1 = 0x3C
LWP_NODE_TYPE_GAS_STEPPER_MOTOR_2 = 0x3D
LWP_NODE_TYPE_GAS_STEPPER_MOTOR_3 = 0x3E
LWP_NODE_TYPE_GAS_STEPPER_MOTOR_4 = 0x3F
LWP_NODE_TYPE_GAS_STEPPER_MOTOR_5 = 0x40
LWP_NODE_TYPE_GAS_STEPPER_MOTOR_6 = 0x41
LWP_NODE_TYPE_GAS_STEPPER_MOTOR_7 = 0x42
LWP_NODE_TYPE_GAS_STEPPER_MOTOR_8 = 0x43
LWP_NODE_TYPE_GAS_STEPPER_MOTOR_9 = 0x44
LWP_NODE_TYPE_GAS_STEPPER_MOTOR_10 = 0x45


SEND_METHOD_NON_ROUTED = 0x00
SEND_METHOD_CONTROL_COMMAND_DEVICE = 0x01
SEND_METHOD_NODE_TYPE = 0x02