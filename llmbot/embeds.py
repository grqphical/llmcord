import discord


def ai_response_embed(model_name: str, response: str):
    embed = discord.Embed(
        title=f"Response from {model_name}",
        description=response,
        color=discord.Color.blue(),
    )
    return embed
