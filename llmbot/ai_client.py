import aiohttp
import json
import os
import urllib.parse as urlparse
from .config import Config


async def send_query(model: str, query: str, config: Config) -> str:
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
                print("ERROR: ", await response.json())
                return "ERROR OCCURED"

            decoded_response = await response.json()
            ai_response = decoded_response["choices"][0]["message"]["content"]
            return ai_response
