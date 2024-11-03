from plugins import BaseClient
import aiohttp
import json


class OpenAIClient(BaseClient):
    def __init__(self) -> None:
        pass

    async def get_response(
        model: str,
        query: str,
        base_url: str,
        token: str,
        system_prompt: str,
        file_url: str,
        context: list[dict],
    ) -> tuple[str, bool]:
        url = base_url + "v1/chat/completions"
        async with aiohttp.ClientSession(json_serialize=json.dumps) as session:
            current_message = {"role": "user", "content": query}

            if file_url:
                current_message["content"] = [
                    {"type": "text", "text": query},
                    {"type": "image_url", "image_url": {"url": file_url}},
                ]

            messages = [
                {"role": "system", "content": system_prompt},
            ]
            messages += context
            messages += current_message

            async with session.post(
                url,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}",
                },
                json={
                    "model": model,
                    "messages": messages,
                    "stream": False,
                },
            ) as response:
                if not response.ok:
                    match response.status:
                        case 429:
                            return (
                                "ERROR: You have been ratelimited. Try again later or buy more credits",
                                False,
                            )
                        case 404:
                            return (
                                "ERROR: Unable to locate API endpoint. Make sure the API is compatible with OpenAI's API",
                                False,
                            )
                        case 500:
                            return (
                                "ERROR: Unable to reach API due to server side issues",
                                False,
                            )
                        case 502:
                            return (
                                "ERROR: Unable to reach API due to server side issues",
                                False,
                            )
                        case 503:
                            return (
                                "ERROR: Unable to reach API due to server side issues",
                                False,
                            )
                        case _:
                            return "ERROR: " + await response.text(), False

                decoded_response = await response.json()
                ai_response = decoded_response["choices"][0]["message"]["content"]
                return ai_response, True
