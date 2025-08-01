import discord
import os
import logging
import asyncio
from dotenv import load_dotenv
from discord.ext import commands

discord.utils.setup_logging()
logger = logging.getLogger("llmcord")

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.moderation = True

bot = commands.Bot(command_prefix="$", intents=intents)


@bot.event
async def on_ready():
    cmds = await bot.tree.sync()

    logger.info(f"Synced {len(cmds)} commands")
    logger.info(f"Logged in as {bot.user}")


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    embeds = bot.get_cog("Embeds")

    if isinstance(error, commands.CommandInvokeError):
        error = error.original

    await ctx.send(embed=embeds.error(error))

    logger.error(error)


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            logger.info(f"Loaded cog '{filename[:-3]}'")


async def main():
    async with bot:
        await load()
        await bot.start(token=os.getenv("TOKEN"))


asyncio.run(main())
