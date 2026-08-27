from levels import (
    level_01, level_02, level_03, level_04, level_05,
    level_06, level_07, level_08, level_09, level_10,
    level_11, level_12, level_13, level_14, level_15,
    level_16, level_17, level_18, level_19, level_20,
)

_MODULES = [
    level_01, level_02, level_03, level_04, level_05,
    level_06, level_07, level_08, level_09, level_10,
    level_11, level_12, level_13, level_14, level_15,
    level_16, level_17, level_18, level_19, level_20,
]

LEVELS = {module.LEVEL_NUMBER: module for module in _MODULES}


def get_level(number):
    return LEVELS[number]


def get_all_numbers():
    return sorted(LEVELS.keys())
