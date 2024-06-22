import aiohttp
import os
import json

SYSTEM_PROMPT = """You are designed to help people on the chat platform Discord. Format your messages using markdown if needed."""


async def send_query(model: str, query: str) -> str:
    async with aiohttp.ClientSession(json_serialize=json.dumps) as session:
        async with session.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f'Bearer {os.getenv("GROQ_TOKEN")}',
            },
            json={
                "model": model,
                "messages": [{"role": "system", "content": SYSTEM_PROMPT}],
                "stream": False,
            },
        ) as response:
            if not response.ok:
                print("ERROR: ", await response.json())
                return "ERROR OCCURED"

            decoded_response = await response.json()
            ai_response = decoded_response["choices"][0]["message"]["content"]
            return ai_response
