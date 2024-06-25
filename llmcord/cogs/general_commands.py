import discord
from discord import app_commands
from discord.ext import commands
from ..config import Config
from ..context import Context
from ..embeds import *


class GeneralCommands(commands.Cog):
    def __init__(self, bot, config: Config, context: Context):
        self.bot = bot
        self.config = config
        self.context = context

    @app_commands.command(name="reload", description="Reloads the configuration file")
    async def reload_config(self, interaction: discord.Interaction):
        self.config = Config()
        await interaction.response.send_message(embed=info_embed("Reloaded config"))
