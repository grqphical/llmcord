import os
import traceback
from importlib import util


class BaseClient:
    """Base plugin class. Every LLM client must inherit from this class"""

    plugins = {}

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.plugins[cls.__name__] = cls

    async def get_response(
        model: str,
        query: str,
        base_url: str,
        token: str,
        system_prompt: str,
        context: list[dict],
    ) -> tuple[str, bool]:
        """Fetches the LLM's response. Returns a tuple containing the response text and a boolean indicating if the request was successful.

        If it was not successful, response should be an error message
        """
        pass


def load_module(path):
    name = os.path.split(path)[-1]
    spec = util.spec_from_file_location(name, path)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


path = os.path.abspath(__file__)
dirpath = os.path.dirname(path)

for fname in os.listdir(dirpath):
    # Load only "real modules"
    if (
        not fname.startswith(".")
        and not fname.startswith("__")
        and fname.endswith(".py")
    ):
        try:
            load_module(os.path.join(dirpath, fname))
        except Exception:
            traceback.print_exc()
