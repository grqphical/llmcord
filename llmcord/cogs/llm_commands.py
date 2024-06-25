import discord
from discord import app_commands
from discord.ext import commands
from ..ai_client import send_query
from ..embeds import *
from ..config import Config
from ..context import Context
from ..logging import logger
from ..views import *


class LLMCommands(commands.Cog):
    def __init__(self, bot, config: Config, context: Context):
        self.bot = bot
        self.config = config
        self.context = context

    async def model_autocomplete(self, interaction: discord.Interaction, current: str):
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
        choices = self.config.get_models()
        return [
            app_commands.Choice(name=choice, value=choice)
            for choice, _ in choices
            if current.lower() in choice.lower()
        ]

    @app_commands.command(
        name="ask",
        description="Ask a LLM a query. Uses the models you have defined in your llmcord.toml file",
    )
    @app_commands.describe(model="Choose a LLM")
    @app_commands.autocomplete(model=model_autocomplete)
    async def ask(
        self, interaction: discord.Interaction, query: str, model: str = None
    ):
        model = model or self.config.default_model
        await interaction.response.defer()
        response, ok = await send_query(
            model, query, self.config, self.context, interaction.channel_id
        )
        if not ok:
            logger.error(f"Failed to send query to {model}")
            await interaction.followup.send(embed=error_embed(response))
            return

        self.context.add_context_message(query, "user", interaction.channel_id)
        self.context.add_context_message(response, "assistant", interaction.channel_id)
        await interaction.followup.send(embed=ai_response_embed(model, response))
        logger.info(f"Sent query to {model}")

    async def model_autocomplete(self, interaction: discord.Interaction, current: str):
        choices = self.config.get_models()
        return [
            app_commands.Choice(name=choice, value=choice)
            for choice, _ in choices
            if current.lower() in choice.lower()
        ]

    @app_commands.command(name="list", description="Lists all defined models")
    async def list_models(self, interaction: discord.Interaction):
        models = self.config.get_models()
        if len(models) <= 8:
            await interaction.response.send_message(embed=model_list_embed(models, 0))
        else:
            view = ModelsListView(models)
            await interaction.response.send_message(
                embed=view.get_current_page(), view=view
            )

    @app_commands.command(
        name="clearcontext", description="Clears this channel's context messages"
    )
    async def clear_context(self, interaction: discord.Interaction):
        self.context.clear(interaction.channel_id)
        await interaction.response.send_message(
            embed=info_embed("Cleared this channel's context")
        )
        logger.info("Cleared context")

    @app_commands.command(
        name="context", description="Shows the current channel's context"
    )
    async def context_list(self, interaction: discord.Interaction):
        ctx = self.context.get_context(interaction.channel_id)
        if len(ctx) <= 8:
            await interaction.response.send_message(embed=context_list_embed(ctx, 0))
        else:
            view = ContextListView(ctx)
            await interaction.response.send_message(
                embed=view.get_current_page(), view=view
            )
