"""LLMCord"""

import tomllib
import logging
import os

CONFIG_FILE = "llmcord.toml"


class Config:
    """
    Represents the configuration settings for the llmbot application.
    """

    def __init__(self) -> None:
        if not os.path.exists(CONFIG_FILE):
            logging.getLogger("llmcord").critical(
                "No config file found. Make sure you have a non-empty file called 'llmcord.toml' \
                    in the same directory as the scripts"
            )
            exit(1)
        with open(CONFIG_FILE, "rb") as f:
            config = tomllib.load(f)

        self.models = {}
        self.system_prompt = config.get("system_prompt")
        self.default_model = config.get("default_model")

        for name, model in config.get("models", {}).items():
            self.models[name] = model

        if self.default_model not in self.models:
            logging.getLogger("llmcord").critical("Default model does not exist")
            exit(1)

        logging.getLogger("llmcord").info("Loaded config")

    def get_model_params(self, name: str) -> tuple[str, str, str, str]:
        """
        Retrieves the model parameters for the specified model name.

        Args:
            name (str): The name of the model.

        Returns:
            tuple[str, str, str, str]: A tuple containing the model, base URL, token and client.
        """
        model = self.models.get(name, None)

        if model is None:
            return (None, None, None, None)

        return (
            model.get("model"),
            model.get("base_url"),
            model.get("token"),
            model.get("client", None),
        )

    def get_models(self) -> list[tuple[str, str]]:
        """
        Retrieves the available models as a list of tuples.

        Returns:
            list[tuple[str, dict]]: A list of tuples containing the model display name and \
                model data.
        """
        result = []
        for name, model in self.models.items():
            result.append((name, model))

        return result
