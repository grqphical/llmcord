import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from .config import Config
from .context import Context
from .logging import logger
from .cogs.general_commands import GeneralCommands
from .cogs.llm_commands import LLMCommands

load_dotenv()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
config = Config()
context = Context()

if config.default_model is None:
    logger.critical("No default model configured")
    exit(1)

if config.system_prompt is None:
    logger.warning("No system prompt has been set up. It will be left empty")
    config.system_prompt = ""


@bot.event
async def on_ready():
    await bot.add_cog(LLMCommands(bot, config, context))
    await bot.add_cog(GeneralCommands(bot, config, context))
    await bot.tree.sync()
    logger.info(f"Logged in as {bot.user}")


bot.run(os.getenv("DISCORD_TOKEN"), log_handler=None)
