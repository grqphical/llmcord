from typing import Coroutine
from plugins import BaseClient
import aiohttp
import json


class GeminiClient(BaseClient):
    async def get_response(
        model: str,
        query: str,
        base_url: str,
        token: str,
        system_prompt: str,
        file_url: str,
        context: list[dict],
    ):
        url = base_url + f"v1beta/models/{model}:generateContent"
        async with aiohttp.ClientSession(json_serialize=json.dumps) as session:
            messages = [
                {"role": "system", "content": system_prompt},
            ]
            messages += context
            messages += [{"role": "user", "content": query}]

            gemini_messages = []
            for message in messages:
                role = "model" if message["role"] == "assistant" else "user"
                gemini_messages.append(
                    {"role": role, "parts": [{"text": message["content"]}]}
                )

            payload = {"contents": gemini_messages}
            async with session.post(
                url,
                json=payload,
                params={"key": token},
                headers={
                    "Content-Type": "application/json",
                },
            ) as response:
                if not response.ok:
                    return "ERROR: " + await response.text(), False

                decoded_response = await response.json()
                ai_response = decoded_response["candidates"][0]["content"]["parts"][0][
                    "text"
                ]
                return ai_response, True
