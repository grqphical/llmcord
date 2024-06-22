from discord import app_commands
import discord
import os
from dotenv import load_dotenv
from .ai_client import send_query
from .embeds import *
from .config import Config
from .views import ModelsListView

load_dotenv()

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
config = Config(os.path.join(os.getcwd(), "llmcord.toml"))


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


@tree.command(
    name="ask",
    description="Ask a LLM a query. Uses the models you have defined in your llmcord.toml file",
)
@app_commands.choices(model=config.get_models_choices())
async def ask(
    interaction: discord.Interaction, model: app_commands.Choice[str], query: str
):
    response = await send_query(model.value, query, config)
    await interaction.response.send_message(
        embed=ai_response_embed(model.name, response)
    )


@tree.command(name="list", description="Lists all defined models")
async def list(interaction: discord.Interaction):
    models = config.get_models()
    if len(models) <= 8:
        await interaction.response.send_message(embed=model_list_embed(models, 1))
    else:
        view = ModelsListView(models)
        await interaction.response.send_message(
            embed=view.get_current_page(), view=view
        )


client.run(os.getenv("DISCORD_TOKEN"))
