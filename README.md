<p align="center">
    <img src="https://github.com/grqphical/llmcord/blob/main/llmcord_logo.png" width="256" height="256"/>
</p>

[![License](https://img.shields.io/github/license/grqphical/llmcord)](https://img.shields.io/github/license/grqphical/llmcord)
[![Version](https://img.shields.io/github/v/release/grqphical/llmcord)](https://img.shields.io/github/v/release/grqphical/llmcord)
[![Size](https://img.shields.io/github/repo-size/grqphical/llmcord)](https://img.shields.io/github/repo-size/grqphical/llmcord)

# LLMCord - An LLM client as a discord bot

This bot allows you to use LLMs such as ChatGPT, LLaMA3, and Gemini 1.5 from Discord.

You are also able to use models such as LLama 3.2 Vision however image generation is not supported (yet!)

## Installation

### Using pre-created executables

Download the executable for the latest release from [Releases](https://github.com/grqphical/llmcord/releases)

**NOTE:** Currently MacOS and Linux do not have pre built binaries

### Manual

1. Clone this repo or download the source code from one of the [Releases](https://github.com/grqphical/llmcord/releases)

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

### Converting to binary

If you want to convert the script into a binary run `pyinstaller llmcord.spec`

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

`model` - Which model to use. Only letters, numbers, underscores and dashses are valid characters here **REQUIRED**

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

### 1.4.0

- Added file upload support for models with vision capabilities

- Moved away from cogs API, will rework later on

- Updated discord.py

- Added the ability to see more detailed log if you set APP_ENV equal to 'dev'

### 1.3.1

- Changed license from MIT to Mozilla Public License 2.0

- Added license to about section of bot

- Bump aiohttp from 3.9.5 to 3.10.2 by @dependabot in https://github.com/grqphical/llmcord/pull/3

- Added PyInstaller spec

### 1.3.0

- Added compare command that allows you to send a response to two LLM's and compare their responses

- Added about command

- Improved Documentation

- Added build scripts

### 1.2.3

- Refactored code to work with Pyinstaller

- Pre built executables are now able to be distrubuted

### 1.2.2

- Moved commands into their own Cogs

- Added unit tests for Config and Context

- Fixed linting errors

- Added CI for unit tests

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

Make sure to install `requirements.txt` then run `pytest` to run the tests.

## Roadmap

I may or may not add these features later on.

- [x] Custom API Handlers (ability to define your own plugins to work with non-OpenAI compatible APIs)

- [x] File uploads

- [ ] Integration with non LLM's (eg. DALL-E for image generation)

## License

LLMCord is licensed under the [Mozilla Public License 2.0](https://github.com/grqphical/llmcord/blob/main/LICENSE)
