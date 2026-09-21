import platform

from masonite import __version__ as masonite_version
from masonite.controllers import Controller
from masonite.views import View


class WelcomeController(Controller):
    def show(self, view: View):
        return view.render(
            "welcome",
            {
                "version": masonite_version,
                "python_version": platform.python_version(),
            },
        )
