from discord import app_commands
import discord
import os
from dotenv import load_dotenv
from .ai_client import send_query
from .embeds import *
from .config import Config

load_dotenv()

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
config = Config(os.path.join(os.getcwd(), "llmbot.toml"))


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
    name="groq",
    description="Ask a LLM from groq a query. Includes LLaMA3, Mixtral 8x7b, and Gemma 7b",
)
@app_commands.choices(model=config.get_models_choices())
async def ask(
    interaction: discord.Interaction, model: app_commands.Choice[str], query: str
):
    response = await send_query(model.value, query, config)
    await interaction.response.send_message(
        embed=ai_response_embed(model.name, response)
    )


client.run(os.getenv("DISCORD_TOKEN"))
