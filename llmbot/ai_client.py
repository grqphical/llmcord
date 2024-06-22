import aiohttp
import json
import os
import urllib.parse as urlparse
from .config import Config


async def send_query(model: str, query: str, config: Config) -> tuple[str, bool]:
    """
    Sends a query to the AI model for completion and returns the AI's response.

    Args:
        model (str): The name of the AI model to use.
        query (str): The user's query.
        config (Config): An instance of the Config class.

    Returns:
        str: The AI's response to the query.
        bool: Whether or not the request succeeded
    """
    model, base_url, token = config.get_model_params(model)
    url = base_url + "v1/chat/completions"
    async with aiohttp.ClientSession(json_serialize=json.dumps) as session:
        async with session.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": config.system_prompt},
                    {"role": "user", "content": query},
                ],
                "stream": False,
            },
        ) as response:
            if not response.ok:
                return "ERROR: " + response.text(), False

            decoded_response = await response.json()
            ai_response = decoded_response["choices"][0]["message"]["content"]
            return ai_response, True
