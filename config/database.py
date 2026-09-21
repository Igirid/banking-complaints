from masoniteorm.connections import ConnectionResolver
from masonite.environment import env

DATABASES = {
    "default": env("DB_CONNECTION", "sqlite"),
    "sqlite": {
        "driver": "sqlite",
        "database": env("SQLITE_DB_DATABASE", "database.sqlite3"),
        "prefix": "",
        "log_queries": env("DB_LOG", False),
    },
    "mysql": {
        "driver": "mysql",
        "host": env("DB_HOST", "127.0.0.1"),
        "port": env("DB_PORT", "3306"),
        "database": env("DB_DATABASE", "masonite"),
        "user": env("DB_USERNAME", "root"),
        "password": env("DB_PASSWORD", ""),
        "prefix": "",
        "grammar": "mysql",
        "options": {"charset": "utf8mb4"},
        "log_queries": env("DB_LOG", False),
    },
    "postgres": {
        "driver": "postgres",
        "host": env("DB_HOST", "127.0.0.1"),
        "port": env("DB_PORT", "5432"),
        "database": env("DB_DATABASE", "masonite"),
        "user": env("DB_USERNAME", "postgres"),
        "password": env("DB_PASSWORD", ""),
        "prefix": "",
        "grammar": "postgres",
        "log_queries": env("DB_LOG", False),
    },
}

DB = ConnectionResolver().set_connection_details(DATABASES)
