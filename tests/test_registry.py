from levels import registry


def test_all_numbers_sorted_and_match_module_attribute():
    numbers = registry.get_all_numbers()
    assert numbers == sorted(numbers)
    for number in numbers:
        module = registry.get_level(number)
        assert module.LEVEL_NUMBER == number
        assert module.get_exercises()
        assert module.TIME_LIMIT_SECONDS > 0
