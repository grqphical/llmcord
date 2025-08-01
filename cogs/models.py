from dataclasses import dataclass
from discord.ext import commands
import discord
import requests
import logging
import tomllib
from urllib.parse import urljoin
from pathlib import Path

CONFIGUATION_PATHS = [
    Path.cwd().joinpath("llmcord.toml"),
    Path.home().joinpath("llmcord.toml"),
]


class ConfigError(Exception):
    """Raised when an issue occurs while parsing LLMCord's configuration"""

    def __init__(self, message):
        self.message = message
        super().__init__(message)


@dataclass
class Model:
    id: str
    owned_by: str
    provider: str
    context_window: int


class Models(commands.Cog):
    def __init__(self):
        super().__init__()

        self.models = {}
        self.default_model = ""

        logger = logging.getLogger("llmcord")

        config_file = ""
        for config_path in CONFIGUATION_PATHS:
            if Path.exists(config_path):
                config_file = str(config_path)

        if config_file == "":
            raise FileNotFoundError(
                f"could not find 'llmcord.toml' in current directory or in user's home directory"
            )

        with open(config_file, "rb") as f:
            data = tomllib.load(f)
        logger.info(f"loaded config from '{config_file}'")

        providers = data.get("providers", {})
        if providers == {}:
            raise ConfigError("no providers defined")

        for name, provider in providers.items():
            self.get_models_from_provider(provider["base_url"], name, provider["token"])

        if data.get("default_model", None) == None:
            self.default_model = self.models.keys()[0]

    def get_models_from_provider(
        self, provider_url: str, provider_name: str, provider_token: str
    ):
        models_url = urljoin(provider_url, "v1/models")

        response = requests.get(
            models_url,
            headers={
                "Authorization": f"Bearer {provider_token}",
            },
        )

        if not response.ok:
            raise ConnectionError(
                f"Unable to retrieve model list from provider: {provider_name}: {response.content}"
            )

        models = response.json().get("data", [])

        for model in models:
            self.models[model["id"]] = Model(
                model["id"], model["owned_by"], provider_name, model["context_window"]
            )


async def setup(bot):
    await bot.add_cog(Models())
