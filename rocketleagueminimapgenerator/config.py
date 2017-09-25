import enum
import math
import os

from ruamel.yaml import YAML


class GenConst(enum.Enum):
    size_modifier = 16

    ball_size = 32 / math.log(size_modifier, 2)
    car_size = 32 / math.log(size_modifier, 2)
    text_size = 64 / math.log(size_modifier, 2)
    center_size = 128 / math.log(size_modifier, 2)


def get_config(key):
    if os.access('config.yml', os.R_OK):
        with open('config.yml') as config_file:
            yaml = YAML(typ='safe')
            config = yaml.load(config_file)['config']
        if key in config.keys():
            return config[key]
        else:
            return GenConst[key].value
    else:
        return GenConst[key].value
