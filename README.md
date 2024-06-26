<p align="center">
    <img src="https://github.com/grqphical/llmcord/blob/main/llmcord_logo.png" width="256" height="256"/>
</p>

[![Pytest](https://github.com/grqphical/llmcord/actions/workflows/python-test.yml/badge.svg)](https://github.com/grqphical/llmcord/actions/workflows/python-test.yml)

# LLMCord - An LLM client as a discord bot

This bot allows you to use LLMs such as ChatGPT, LLaMA3, and Gemini 1.5 from Discord

## Installation

1. Clone this repo

```bash
$ git clone https://github.com/grqphical/LLMCord.git
```

2. Create a virtual environment

```bash
$ python -m venv venv
```

3. Activate the virtual environment

```bash
$ ./venv/Scripts/activate
```

**NOTE** On linux the path will be `./venv/bin/activate`

4. Install dependencies

```bash
$ pip install -r requirements.txt
```

### Why no executable to download?

I tried to compile these Python scripts into an executable however it wouldn't work. If anyone can get one working please create an issue with the method you used.

Not having an executable also ensures that it works across all platforms without needing me to compile versions for every platform.

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
client = "OpenAIClient"
```

**NOTE** I am using Groq AI here as an example so I have selected the `OpenAIClient` due to it's API being compatible with OpenAI however LLMCord also includes a Google Gemini 1.5 client that you can use as `GeminiClient`

### Explanation of config

`system_prompt` - Allows you to control the system prompt of the AI

`default_model` - Specifies the default model **REQUIRED**

For each model you wish to make create it as a seperate table with a display name. In this case I chose `llama3-70b`.
`base_url` - Base URL for the API **REQUIRED**

`model` - Which model to use **REQUIRED**

`token` - API token for API, **REQUIRED IF NEEDED BY API**

`client` - Which Client to use to send the request. The two included clients are `OpenAIClient` and `GeminiClient`. **REQUIRED**

### Then finally run

```bash
$ python -m llmcord
```

Now you should be able to use LLMCord in any servers you have invited it to.

## Contributing

See [CONTRIBUTING.md](https://github.com/grqphical/llmcord/blob/main/CONTRIBUTING.md)

## Plugins/Custom Clients

You are able to make your own API clients by creating a python script in the `plugins/` folder. Simply create a class that inherits from `plugins.BaseClient` and implement
the `get_response` method. Make sure it is a coroutine. In order to access the API use the `aiohttp` library as it is already installed and used by LLMCord.

Look in the plugins folder for examples of custom clients

## Changelog

### 1.2.1

- Fixed error handling with certain edge cases when loading the configuration

- Added error handling when selecting an invalid/undefined model. Before it would just get stuck in an infinite loop

- Improved documentation

### 1.2.0

- Added custom logger

### 1.1.0

- Added support for custom clients

- Included `OpenAIClient` and `GeminiClient` by default

- Changed `/list` to now show every model on a different line

## Running the test suite

Make sure to install both `requirements.txt` and `requirements.tests.txt`. Then run `pytest` to run the tests.

## Roadmap

I may or may not add these features later on so feel free to make a PR and implement these features.

- [x] Custom API Handlers (ability to define your own plugins to work with non-OpenAI compatible APIs)

- [ ] File uploads

- [ ] Integration with non LLM's (eg. DALL-E for image generation)

## License

LLMCord is licensed under the MIT License
