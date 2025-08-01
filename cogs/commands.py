from discord.ext import commands
from discord import app_commands
from typing import List
import discord


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def model_list_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> List[app_commands.Choice]:
        return [
            discord.app_commands.Choice(
                name=f"{model.id} ({model.provider})", value=model.id
            )
            for model in self.bot.get_cog("Models").models.values()
            if current.lower() in model.id.lower()
        ]

    @app_commands.command(
        name="chat", description="Creates a new conversation with an LLM"
    )
    @app_commands.autocomplete(model=model_list_autocomplete)
    async def chat(self, interaction: discord.Interaction, model: str):
        await interaction.response.send_message(f"Created new chat with {model}")


async def setup(bot):
    await bot.add_cog(Commands(bot))
