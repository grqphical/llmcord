import discord
from discord.ext import commands


class Embeds(commands.Cog):
    def __init__(self):
        super().__init__()

    def error(self, msg):
        return discord.Embed(
            title="LLMCord Error", description=f"{msg}", color=discord.Color.red()
        )


async def setup(bot):
    await bot.add_cog(Embeds())
