"""Logging Config"""

CHANNELS = {
    "default": {
        "driver": "console",
        "level": "info",
        "timezone": "UTC",
        "format": "{timestamp} - {levelname}: {message}",
        "date_format": "YYYY-MM-DD HH:mm:ss",
        # propagate messages to ancestor (root) Python loggers. Can be
        # overriden per channel. Disabled by default to avoid duplicates.
        "propagate": False,
    },
    "console": {
        "driver": "terminal",
    },
    "single": {
        "driver": "single",
        "path": "storage/logs/masonite.log",
    },
    "daily": {
        "driver": "daily",
        "path": "storage/logs/daily.log",
        "days": 7,
        "keep": 10,
    },
    "stack": {"driver": "stack", "channels": ["single", "console"]},
    "syslog": {"driver": "syslog", "address": "/var/log/system.log"},
    "slack": {
        "driver": "slack",
        "webhook_url": "",
    },
}
