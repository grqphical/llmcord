import discord


def ai_response_embed(model_name: str, response: str):
    embed = discord.Embed(
        title=f"Response from {model_name}",
        description=response,
        color=discord.Color.blue(),
    )
    return embed

def error_embed(error_message: str):
    embed = discord.Embed(
        title="Error",
        description=error_message,
        color=discord.Color.red()
    )
    return embed

def model_list_embed(models: list[tuple[str, str]], page_num: int):
    if page_num == 0:
        embed = discord.Embed(title=f"Models", color=discord.Color.blue())
    else:
        embed = discord.Embed(
            title=f"Models Page {page_num}", color=discord.Color.blue()
        )
    for model in models:
        embed.add_field(name=model[0], value=f"{model[1]["model"]} at {model[1]["base_url"]}")
    return embed
