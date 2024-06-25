import pytest
import sys
import os

sys.path.append("..")
from llmcord.context import Context


@pytest.fixture()
def init():
    try:
        os.remove("context.pkl")
    except:
        pass
    ctx = Context()
    ctx.context["1"] = [{"role": "user", "content": "test"}]
    yield ctx


class TestContext:
    def test_add_message(self, init: Context):
        init.add_context_message("test", "user", "2")
        assert init.context["2"] == [{"role": "user", "content": "test"}]

    def test_get_context(self, init: Context):
        ctx = init.get_context("1")
        assert ctx == [{"role": "user", "content": "test"}]

    def test_clear_context(self, init: Context):
        init.clear("2")
        assert init.get_context("2") == []
