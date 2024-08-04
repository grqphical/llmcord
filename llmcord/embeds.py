"""LLMCord"""
import discord
from llmcord import __version__

def ai_response_embed(model_name: str, response: str):
    embed = discord.Embed(
        title=f"Response from {model_name}",
        description=response,
        color=discord.Color.blue(),
    )
    return embed

def info_embed(message: str):
    embed = discord.Embed(
        title="Info",
        description=f"ℹ️ {message}",
        color=discord.Color.green()
    )
    return embed

def error_embed(error_message: str):
    embed = discord.Embed(
        title="Error",
        description=f"❌ {error_message}",
        color=discord.Color.red()
    )
    return embed

def model_list_embed(models: list[tuple[str, str]], page_num: int):
    if page_num == 0:
        embed = discord.Embed(title="Models", color=discord.Color.blue())
    else:
        embed = discord.Embed(
            title=f"Models Page {page_num}", color=discord.Color.blue()
        )
    for model in models:
        embed.add_field(name=model[0], value=f"{model[1]["model"]} at {model[1]["base_url"]}", inline=False)
    return embed


def context_list_embed(context: list[dict], page_num: int):
    if page_num == 0:
        embed = discord.Embed(title="Context", color=discord.Color.blue())
    else:
        embed = discord.Embed(
            title=f"Context Page {page_num}", color=discord.Color.blue()
        )
    for msg in context:
        embed.add_field(name=msg["role"], value=msg["content"], inline=False)
    return embed

def two_result_embed(response1: str, response2: str, model1: str, model2: str):
    embed = discord.Embed(title="Responses", color=discord.Color.blue())

    embed.add_field(name=model1, value=response1, inline=True)
    embed.add_field(name=model2, value=response2, inline=True)

    return embed

def about_embed():
    embed = discord.Embed(title="About LLMCord", color=discord.Color.blue())
    embed.set_thumbnail(url="https://raw.githubusercontent.com/grqphical/llmcord/main/llmcord_logo.png")
    embed.add_field(name="Version", value=f"{__version__}", inline=False)
    embed.add_field(name="Author", value="grqphical", inline=False)
    embed.add_field(name="Repo", value="https://github.com/grqphical/llmcord", inline=False)
    return embed
