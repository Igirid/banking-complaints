from masonite.providers import (
    AuthenticationProvider,
    AuthorizationProvider,
    BroadcastProvider,
    CacheProvider,
    EventProvider,
    ExceptionProvider,
    FrameworkProvider,
    HashServiceProvider,
    HelpersProvider,
    MailProvider,
    ORMProvider,
    PresetsProvider,
    QueueProvider,
    RateProvider,
    RouteProvider,
    SessionProvider,
    StorageProvider,
    ViewProvider,
    WhitenoiseProvider,
)
from masonite.scheduling.providers import ScheduleProvider
from masonite.notification.providers import NotificationProvider
from masonite.validation.providers import ValidationProvider
from masonite.logging import LoggingProvider

# from masonite.api.providers import ApiProvider

from app.providers.AppProvider import AppProvider

PROVIDERS = [
    FrameworkProvider,
    HelpersProvider,
    RateProvider,
    RouteProvider,
    ViewProvider,
    WhitenoiseProvider,
    ExceptionProvider,
    MailProvider,
    NotificationProvider,
    SessionProvider,
    CacheProvider,
    QueueProvider,
    ScheduleProvider,
    EventProvider,
    StorageProvider,
    BroadcastProvider,
    HashServiceProvider,
    AuthenticationProvider,
    AuthorizationProvider,
    ValidationProvider,
    PresetsProvider,
    ORMProvider,
    LoggingProvider,
    # ApiProvider,
    AppProvider,
]
