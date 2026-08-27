from levels import registry


def test_all_numbers_sorted_and_match_module_attribute():
    numbers = registry.get_all_numbers()
    assert numbers == sorted(numbers)
    for number in numbers:
        module = registry.get_level(number)
        assert module.LEVEL_NUMBER == number
        assert module.get_exercises()
        assert module.TIME_LIMIT_SECONDS > 0


def test_falling_mode_levels_declare_seconds_per_character():
    for number in registry.get_all_numbers():
        module = registry.get_level(number)
        if getattr(module, "FALLING_MODE", False):
            assert module.SECONDS_PER_CHARACTER > 0, module.NAME


def test_levels_11_to_20_are_falling_mode():
    for number in range(11, 21):
        module = registry.get_level(number)
        assert module.FALLING_MODE is True, module.NAME
