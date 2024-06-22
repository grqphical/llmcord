import tomllib
from discord import app_commands


class Config:
    def __init__(self, file: str) -> None:
        with open(file, "rb") as f:
            config = tomllib.load(f)

        self.models = {}
        self.system_prompt = config["system_prompt"]

        for name, model in config["models"].items():
            self.models[name] = model

    def get_model_params(self, name: str) -> tuple[str, str, str]:
        model = self.models[name]
        return model["model"], model["base_url"], model["token_name"]

    def get_models_choices(self) -> list[app_commands.Choice]:
        result = []
        for name in self.models.keys():
            result.append(app_commands.Choice(name=name, value=name))

        return result
