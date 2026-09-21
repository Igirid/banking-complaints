"""User Model."""

from masoniteorm.models import Model
from masonite.authentication import Authenticates
from masonite.authorization import Authorizes
from masonite.notification import Notifiable


class User(Model, Authenticates, Authorizes, Notifiable):
    """User Model."""

    __fillable__ = ["name", "email", "password", "phone"]
    __hidden__ = ["password"]
    __auth__ = "email"
