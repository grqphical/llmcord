# LLMCord - An LLM client as a discord bot

This bot allows you to use LLMs such as ChatGPT, LLaMA3, and Gemma from Discord

## Installation

Clone this repo, create a virtualenv, and run

```bash
$ pip install -r requirements.txt
```

## Usage

1. Create a new Discord Application at the Discord Developer Portal and configure it to be a bot. (Guide [Here](https://discordpy.readthedocs.io/en/stable/discord.html))
2. Create a .env file and add your bot's token as `DISCORD_TOKEN`
3. Create a file called `llmcord.toml` and add this to it:

```toml
system_prompt = "Use markdown if neccessary."
default_model = "llama3-70b"

[models.llama3-70b]
base_url = "https://api.groq.com/openai/"
model = "llama3-70b-8192"
token = "API_TOKEN_HERE"
```

**NOTE** I am using Groq AI here as an example however LLMCord will work with any OpenAI compatible API

### Explanation of config

`system_prompt` - Allows you to control the system prompt of the AI
`default_model` - Specifies the default model **REQUIRED**

For each model you wish to make create it as a seperate table with a display name. In this case I chose `llama3-70b`.
`base_url` - Base URL for the API **REQUIRED**
`model` - Which model to use **REQUIRED**
`token` - API token for API, **REQUIRED IF NEEDED BY API**

### Then finally run

```bash
$ python -m llmcord
```

Now you should be able to use LLMCord in any servers you have invited it to.

## Changelog

No updates yet :|

## Roadmap

- [ ] Custom API Handlers (ability to define your own plugins to work with non-OpenAI compatible APIs)

- [ ] File uploads

- [ ] Integration with non LLM's (eg. DALL-E for image generation)

## License

LLMCord is licensed under the MIT License
