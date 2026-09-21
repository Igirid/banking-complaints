from masonite.foundation import Application, Kernel
from masonite.utils.location import base_path

from app.Kernel import Kernel as ApplicationKernel
from config.providers import PROVIDERS

application = Application(base_path())

"""First bind the important providers needed to start the server."""
application.register_providers(
    Kernel,
    ApplicationKernel,
)

application.add_providers(*PROVIDERS)
