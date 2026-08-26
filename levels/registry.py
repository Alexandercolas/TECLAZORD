from levels import (
    level_01, level_02, level_03, level_04, level_05,
    level_06, level_07, level_08, level_09, level_10,
)

_MODULES = [
    level_01, level_02, level_03, level_04, level_05,
    level_06, level_07, level_08, level_09, level_10,
]

LEVELS = {module.LEVEL_NUMBER: module for module in _MODULES}


def get_level(number):
    return LEVELS[number]


def get_all_numbers():
    return sorted(LEVELS.keys())
