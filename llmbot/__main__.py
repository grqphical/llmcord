from discord import app_commands
import discord
import os
from dotenv import load_dotenv
from .ai_client import send_query
from .embeds import *
from .config import Config
from .views import ModelsListView, ContextListView
from .context import Context

load_dotenv()

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
config = Config(os.path.join(os.getcwd(), "llmcord.toml"))
context = Context()


class ConfigError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def get_model_real_name(display_name: str) -> str:
    model, _, _ = config.get_model_params(display_name)
    return model


if config.default_model == None:
    raise ConfigError("No default model has been set. Set it with `default_model`")


@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user}")
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="Aritifical Intelligence Developments",
        )
    )


async def model_autocomplete(interaction: discord.Interaction, current: str):
    choices = config.get_models()
    return [
        app_commands.Choice(name=choice, value=choice)
        for choice, _ in choices
        if current.lower() in choice.lower()
    ]


@tree.command(
    name="ask",
    description="Ask a LLM a query. Uses the models you have defined in your llmcord.toml file",
)
@app_commands.describe(model="Choose a LLM")
@app_commands.autocomplete(model=model_autocomplete)
async def ask(
    interaction: discord.Interaction, query: str, model: str = config.default_model
):
    """
    Ask a query to a LLM (Language Model). This function uses the models defined in the llmcord.toml file.

    Parameters:
    - interaction: The Discord interaction object.
    - model: The chosen model for the query.
    - query: The query to ask the LLM.

    Returns:
    - None

    Raises:
    - None
    """
    response, ok = await send_query(
        model, query, config, context, interaction.channel_id
    )
    if not ok:
        await interaction.response.send_message(embed=error_embed(response))

    context.add_context_message(query, "user", interaction.channel_id)
    context.add_context_message(response, "assistant", interaction.channel_id)

    await interaction.response.send_message(embed=ai_response_embed(model, response))


@tree.command(name="list", description="Lists all defined models")
async def list(interaction: discord.Interaction):
    models = config.get_models()
    if len(models) <= 8:
        await interaction.response.send_message(embed=model_list_embed(models, 0))
    else:
        view = ModelsListView(models)
        await interaction.response.send_message(
            embed=view.get_current_page(), view=view
        )


@tree.command(name="clearcontext", description="Clears this channels context messages")
async def clear(interaction: discord.Interaction):
    context.clear(interaction.channel_id)
    await interaction.response.send_message(
        embed=info_embed("Cleared this channel's context")
    )


@tree.command(name="context", description="Shows the current channels's context")
async def context_list(interaction: discord.Interaction):
    ctx = context.get_context(interaction.channel_id)
    if len(ctx) <= 8:
        await interaction.response.send_message(embed=context_list_embed(ctx, 0))
    else:
        view = ContextListView(ctx)
        await interaction.response.send_message(
            embed=view.get_current_page(), view=view
        )


client.run(os.getenv("DISCORD_TOKEN"))
