LEVEL_NUMBER = 20
NAME = "SYSTEMS ENGINEER FINAL CHALLENGE"
TIME_LIMIT_SECONDS = 60
FALLING_MODE = True
SECONDS_PER_CHARACTER = 0.20

# El nivel final de la Fase 2: combina todo lo anterior en oraciones
# completas de ingenieria en sistemas. Una en espanol, como haria un
# ingeniero real alternando idiomas en su trabajo diario.
EXERCISES = [
    "The system administrator restarted the server after the crash.",
    "Our database query returned an unexpected null value.",
    "She deployed the microservice using a docker container.",
    "The network engineer configured the firewall rules manually.",
    "This algorithm has a time complexity of O(n log n).",
    "El ingeniero reviso el codigo antes del despliegue final.",
    "The api endpoint returned a 404 error unexpectedly.",
    "We need to optimize this query before the next release.",
]


def get_exercises():
    return EXERCISES
