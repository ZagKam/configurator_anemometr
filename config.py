import configparser
from typing import TypedDict
from resourse_path import resource_path
import json


class Config(TypedDict):
    """Byte commands in ssource must be plain strings wihout CRC.
    The config objeect contains byte commands with CRC32 modbus"""

    motor_configuration_command: bytes
    motor_configuration_answer_size: int
    motor_rotation_commmand: bytes
    motor_rotation_answer_size: int
    motor_rotation_duration: int
    current_off_command: bytes
    current_off_answer_size: int
    get_version_command: bytes
    get_version_answer_size: int
    oporn_signal_set_command: bytes
    oporn_signal_set_duration: int
    oporn_signal_set_answer_size: int
    wind_velocity_coef_duration: int
    calibration_koef_answer_size: int
    calibration_step_number: int
    log_level: int
    test: bool

    
def convert_to_bytes(self):
    
    from get_crc import get_crc
    for i in ("motor_configuration_command", "motor_rotation_commmand",
                "current_off_command", "get_version_command", "oporn_signal_set_command"):
        try:
            request = self[i] + get_crc(self[i])
            self[i] = bytes.fromhex(request)
        except KeyError:
            print(i, "is missing in config")
        

config = Config()

with open(resource_path("config.json"), encoding="utf8") as f:
    config.update(json.load(f))

convert_to_bytes(config)
