LEVEL_NUMBER = 14
NAME = "DATABASES"
TIME_LIMIT_SECONDS = 75
FALLING_MODE = True
SECONDS_PER_CHARACTER = 0.33

EXERCISES = [
    "select from table",
    "primary key",
    "foreign key",
    "join query",
    "index optimization",
    "database schema",
    "stored procedure",
    "query performance",
    "data normalization",
    "transaction rollback",
]


def get_exercises():
    return EXERCISES
