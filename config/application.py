from masonite.environment import env

NAME = env("APP_NAME", "Masonite")

KEY = env("APP_KEY")

DEBUG = env("APP_DEBUG", True)

HASHING = {
    "default": "bcrypt",
    "bcrypt": {"rounds": 10},
    "argon2": {"memory": 1024, "threads": 2, "time": 2},
}

APP_URL = env("APP_URL", "http://localhost:8000/")

MIX_BASE_URL = env("MIX_BASE_URL", None)
