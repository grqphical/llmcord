"""LLMCord"""

__version__ = "1.4.0"

import os
import discord
from discord.ext import commands
import discord.app_commands as app_commands
from dotenv import load_dotenv


from .config import Config
from .context import Context
from .logger import logger
from .ai_client import send_query
from .embeds import *
from .views import *


intents = discord.Intents.all()
config = Config()
context = Context()
bot = commands.Bot(
    intents=intents,
    command_prefix="!",
    activity=discord.Game(name="with different LLMs"),
)

load_dotenv()


async def model_autocomplete(interaction: discord.Interaction, current: str):
    """
    Autocomplete function for the 'model' parameter in the 'ask' command.

    Parameters:
    - interaction: The Discord interaction object.
    - current: The current input for autocomplete.

    Returns:
    - A list of app_commands.Choice objects for autocomplete.

    Raises:
    - None
    """
    choices = config.get_models()
    return [
        app_commands.Choice(name=choice, value=choice)
        for choice, _ in choices
        if current.lower() in choice.lower()
    ]


@bot.event
async def on_ready():
    """Runs when the bot is ready and connected to Discord"""
    logger.info("Logged in as %s", bot.user)
    await bot.tree.sync()


# =============================LLM COMMANDS=============================


@app_commands.describe(
    model="Choose a LLM", file="Upload an image (if the model supports it)"
)
@app_commands.autocomplete(model=model_autocomplete)
@bot.tree.command(
    name="ask",
    description="Ask a LLM a query. Uses the models you have defined in your llmcord.toml file",
)
async def ask(
    interaction: discord.Interaction,
    query: str,
    model: str = None,
    file: discord.Attachment = None,
):
    model = model or config.default_model
    await interaction.response.defer()

    file_url = file.url if file else None

    response, ok = await send_query(
        model, query, file_url, config, context, interaction.channel_id
    )
    if not ok:
        logger.error(f"Failed to send query to {model}")
        await interaction.followup.send(embed=error_embed(response))
        return

    context.add_context_message(query, "user", interaction.channel_id)
    context.add_context_message(response, "assistant", interaction.channel_id)
    await interaction.followup.send(embed=ai_response_embed(model, response))
    logger.info(f"Sent query to {model}")


@bot.tree.command(name="list", description="Lists all defined models")
async def list_models(interaction: discord.Interaction):
    models = config.get_models()
    if len(models) <= 8:
        await interaction.response.send_message(embed=model_list_embed(models, 0))
    else:
        view = ModelsListView(models)
        await interaction.response.send_message(
            embed=view.get_current_page(), view=view
        )


@bot.tree.command(name="context", description="Shows the current channel's context")
async def context_list(interaction: discord.Interaction):
    ctx = context.get_context(interaction.channel_id)
    if len(ctx) <= 8:
        await interaction.response.send_message(embed=context_list_embed(ctx, 0))
    else:
        view = ContextListView(ctx)
        await interaction.response.send_message(
            embed=view.get_current_page(), view=view
        )


@bot.tree.command(name="compare", description="Compare the responses of two LLMs")
@app_commands.describe(model1="Choose a LLM")
@app_commands.autocomplete(model1=model_autocomplete)
@app_commands.describe(model2="Choose a LLM")
@app_commands.autocomplete(model2=model_autocomplete)
async def side_by_side(
    interaction: discord.Interaction, query: str, model1: str, model2: str
):
    await interaction.response.defer()

    # First model response
    response1, ok = await send_query(
        model1, query, None, config, context, interaction.channel_id
    )
    if not ok:
        logger.error(f"Failed to send query to {model1}")
        await interaction.followup.send(embed=error_embed(response1))
        return

    context.add_context_message(query, "user", interaction.channel_id)
    context.add_context_message(response1, "assistant", interaction.channel_id)
    logger.info(f"Sent query to {model1}")

    # Second model response
    response2, ok = await send_query(
        model2, query, None, config, context, interaction.channel_id
    )
    if not ok:
        logger.error(f"Failed to send query to {model2}")
        await interaction.followup.send(embed=error_embed(response2))
        return

    context.add_context_message(response2, "assistant", interaction.channel_id)
    logger.info(f"Sent query to {model2}")

    await interaction.followup.send(
        embed=two_result_embed(response1, response2, model1, model2)
    )


# =============================GENERAL COMMANDS=============================


@bot.tree.command(name="reload", description="Reloads the configuration file")
async def reload_config(interaction):
    global config
    config = Config()
    await interaction.response.send_message(embed=info_embed("Reloaded config"))


@bot.tree.command(name="about", description="Print information about the bot")
async def about(interaction):
    await interaction.response.send_message(embed=about_embed())


# =============================MAIN BOT=============================


def main():
    if config.default_model is None:
        logger.critical("No default model configured")
        exit(1)

    if config.system_prompt is None:
        logger.warning("No system prompt has been set up. It will be left empty")
        config.system_prompt = ""

    if os.getenv("APP_ENV") == "dev":
        bot.run(os.getenv("DISCORD_TOKEN"))
    else:
        bot.run(os.getenv("DISCORD_TOKEN"), log_handler=None)


main()
