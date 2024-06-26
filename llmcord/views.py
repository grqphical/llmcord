import discord
from .embeds import model_list_embed, context_list_embed


def split(list_a, chunk_size):
    for i in range(0, len(list_a), chunk_size):
        yield list_a[i : i + chunk_size]


class ModelsListView(discord.ui.View):
    def __init__(self, models: list[tuple[str, str]]):
        super().__init__()
        self.models = list(split(models, 8))
        self.current_page = 0
        self.total_pages = len(self.models)
        self.current_page_data = self.models[self.current_page]

    async def get_current_page(self) -> discord.Embed:
        return model_list_embed(self.current_page_data, self.current_page + 1)

    async def update_page(self, interaction: discord.Interaction):
        self.current_page_data = self.models[self.current_page]
        await interaction.response.edit_message(
            embed=await self.get_current_page(), view=self
        )

    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.blurple)
    async def previous_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if self.total_pages == 1:
            await interaction.response.edit_message(
                view=self, embed=await self.get_current_page()
            )
            return

        if self.current_page > 0:
            self.current_page -= 1

        await self.update_page(interaction)

    @discord.ui.button(label="➡️", style=discord.ButtonStyle.blurple)
    async def next_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if self.total_pages == 1:
            await interaction.response.edit_message(
                view=self, embed=await self.get_current_page()
            )
            return

        if self.current_page < self.total_pages:
            self.current_page += 1

        await self.update_page(interaction)


class ContextListView(discord.ui.View):
    def __init__(self, context: list[dict]):
        super().__init__()
        self.context = list(split(context, 8))
        self.current_page = 0
        self.total_pages = len(self.context)
        self.current_page_data = self.context[self.current_page]

    async def get_current_page(self) -> discord.Embed:
        return context_list_embed(self.current_page_data, self.current_page + 1)

    async def update_page(self, interaction: discord.Interaction):
        self.current_page_data = self.context[self.current_page]
        await interaction.response.edit_message(
            embed=await self.get_current_page(), view=self
        )

    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.blurple)
    async def previous_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if self.total_pages == 1:
            await interaction.response.edit_message(
                view=self, embed=await self.get_current_page()
            )
            return

        if self.current_page > 0:
            self.current_page -= 1

        await self.update_page(interaction)

    @discord.ui.button(label="➡️", style=discord.ButtonStyle.blurple)
    async def next_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if self.total_pages == 1:
            await interaction.response.edit_message(
                view=self, embed=await self.get_current_page()
            )
            return

        if self.current_page < self.total_pages:
            self.current_page += 1

        await self.update_page(interaction)
