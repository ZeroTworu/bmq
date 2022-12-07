from os import getenv

IDLE_TIMEOUT = float(getenv('BMQ_IDLE_TIMEOUT', 1))
