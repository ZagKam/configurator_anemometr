import configparser
from typing import TypedDict
from resourse_path import resource_path
import json


class Config(TypedDict):
    motor_configuration_command: bytes
    motor_rotation_commmand: bytes
    current_off_command: bytes
    motor_rotation_duration: int
    oporn_signal_set_dduration: int
    wind_velocity_coef_duration: int
    calibration_step_number: int
    log_level: int

    def __init__(self):
        super().__init__()
        with open(resource_path("config.json"), encoding="utf8") as f:
            self = json.load(f)
    
    def convert_to_bytes(self):
        for i in ("motor_configuration_command", "motor_rotation_commmand",
                  "current_off_command"):
            try:
                self[i] = bytes.fromhex(self[i])
            except KeyError:
                print(i, "is missing in config")
        


