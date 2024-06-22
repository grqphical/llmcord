import discord
from .embeds import model_list_embed, context_list_embed


def split(list_a, chunk_size):
    for i in range(0, len(list_a), chunk_size):
        yield list_a[i : i + chunk_size]


"""View used to add pagination to models list embed"""


class ModelsListView(discord.ui.View):
    def __init__(self, models: list[tuple[str, str]]):
        super().__init__()
        self.models = list(split(models))
        self.current_page = 0
        self.total_pages = len(self.models)
        self.current_page_data = self.models[self.current_page]

    """Gets the embed for the current page"""

    async def get_current_page(self) -> discord.Embed:
        return model_list_embed(self.current_page_data, self.current_page + 1)

    """Updates the message to the current page"""

    async def update_page(self, interaction: discord.Interaction):
        self.current_page_data = self.models[self.current_page]
        await interaction.response.edit_message(
            embed=await self.get_current_page(), view=self
        )

    """Button used to go back a page"""

    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.blurple)
    async def previous_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        # If we only have one page just set the pages contents to be the same as we don't need to change them
        if self.total_pages == 1:
            await interaction.response.edit_message(
                view=self, embed=await self.get_current_page()
            )
            return

        # If the user is not at the beginning, decrease the page count by 1
        if self.current_page > 0:
            self.current_page -= 1

        # Finally update the page
        await self.update_page(interaction)

    """Button used to go forward a page"""

    @discord.ui.button(label="➡️", style=discord.ButtonStyle.blurple)
    async def next_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        # If we only have one page just set the pages contents to be the same as we don't need to change them
        if self.total_pages == 1:
            await interaction.response.edit_message(
                view=self, embed=await self.get_current_page()
            )
            return

        # If the user is not at the end, increase the page count by 1
        if self.current_page < self.total_pages:
            self.current_page += 1

        # Finally update the page
        await self.update_page(interaction)

    async def on_timeout(self):
        # remove buttons on timeout
        message = await self.interaction.original_response()
        await message.edit(view=None)


"""View used to add pagination to context list embed"""


class ContextListView(discord.ui.View):
    def __init__(self, context: list[dict]):
        super().__init__()
        self.context = list(split(context))
        self.current_page = 0
        self.total_pages = len(self.context)
        self.current_page_data = self.context[self.current_page]

    """Gets the embed for the current page"""

    async def get_current_page(self) -> discord.Embed:
        return context_list_embed(self.current_page_data, self.current_page + 1)

    """Updates the message to the current page"""

    async def update_page(self, interaction: discord.Interaction):
        self.current_page_data = self.models[self.current_page]
        await interaction.response.edit_message(
            embed=await self.get_current_page(), view=self
        )

    """Button used to go back a page"""

    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.blurple)
    async def previous_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        # If we only have one page just set the pages contents to be the same as we don't need to change them
        if self.total_pages == 1:
            await interaction.response.edit_message(
                view=self, embed=await self.get_current_page()
            )
            return

        # If the user is not at the beginning, decrease the page count by 1
        if self.current_page > 0:
            self.current_page -= 1

        # Finally update the page
        await self.update_page(interaction)

    """Button used to go forward a page"""

    @discord.ui.button(label="➡️", style=discord.ButtonStyle.blurple)
    async def next_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        # If we only have one page just set the pages contents to be the same as we don't need to change them
        if self.total_pages == 1:
            await interaction.response.edit_message(
                view=self, embed=await self.get_current_page()
            )
            return

        # If the user is not at the end, increase the page count by 1
        if self.current_page < self.total_pages:
            self.current_page += 1

        # Finally update the page
        await self.update_page(interaction)

    async def on_timeout(self):
        # remove buttons on timeout
        message = await self.interaction.original_response()
        await message.edit(view=None)
