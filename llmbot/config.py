import tomllib
from discord import app_commands


class Config:
    """
    Represents the configuration settings for the llmbot application.
    """

    def __init__(self, file: str) -> None:
        with open(file, "rb") as f:
            config = tomllib.load(f)

        self.models = {}
        self.system_prompt = config["system_prompt"]

        for name, model in config["models"].items():
            self.models[name] = model

    def get_model_params(self, name: str) -> tuple[str, str, str]:
        """
        Retrieves the model parameters for the specified model name.

        Args:
            name (str): The name of the model.

        Returns:
            tuple[str, str, str]: A tuple containing the model, base URL, and token.
        """
        model = self.models[name]
        return model["model"], model["base_url"], model["token"]

    def get_models_choices(self) -> list[app_commands.Choice]:
        """
        Retrieves the available model choices as a list of app_commands.Choice objects to be used in the Discord slash command.

        Returns:
            list[app_commands.Choice]: A list of app_commands.Choice objects representing the available model choices.
        """
        result = []
        for name in self.models.keys():
            result.append(app_commands.Choice(name=name, value=name))

        return result

    def get_models(self) -> list[tuple[str, str]]:
        """
        Retrieves the available models as a list of tuples.

        Returns:
            list[tuple[str, str]]: A list of tuples containing the model display name and model real name.
        """
        result = []
        for name, model in self.models.items():
            result.append((name, model))

        return result
