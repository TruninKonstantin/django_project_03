from enum import Enum


class Constants(Enum):
    TEMPERATURE_FIELD_NAMES = ['pressure_m29', 'pressure_38', 'pressure_50', 'pressure_100',
        'pressure_150', 'pressure_200', 'pressure_250', 'pressure_300', 'pressure_325', 'pressure_350',
        'pressure_375', 'pressure_400', 'pressure_425']
    LOWEST_TEMPERATURE_FIELD_NAME = "pressure_m29"
    HIGHEST_TEMPERATURE_FIELD_NAME = "pressure_425"
    STR_PART_PRESSURE_FIELD = "pressure_"
    STR_FOR_MINUS = "m"
    NUMBER_POSITION_AFTER_SPLIT = 1
    NUMBER_OF_DECIMALS = 3
