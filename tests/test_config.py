import pytest
import sys

sys.path.append("..")
from llmcord.config import Config, CONFIG_FILE


@pytest.fixture()
def init():
    with open(CONFIG_FILE, "w") as f:
        f.write("default_model = 'gpt4'\n[models.gpt4]")

    config = Config()
    config.models = {
        "gpt4": {
            "model": "gpt4",
            "base_url": "https://example.com",
            "token": "FOO",
            "client": "OpenAIClient",
        }
    }
    config.default_model = "gpt4"
    config.system_prompt = "Use markdown if necessary"
    yield config


class TestConfig:
    def test_get_model_params(self, init: Config):
        model, base_url, token, client = init.get_model_params("gpt4")
        assert model == "gpt4"
        assert base_url == "https://example.com"
        assert token == "FOO"
        assert client == "OpenAIClient"

    def test_get_models(self, init: Config):
        models = init.get_models()
        assert models[0] == (
            "gpt4",
            {
                "model": "gpt4",
                "base_url": "https://example.com",
                "token": "FOO",
                "client": "OpenAIClient",
            },
        )
