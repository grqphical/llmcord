import aiohttp
import json
from .config import Config
from .context import Context


async def send_query(
    model: str, query: str, config: Config, context: Context, channel_id: str
) -> tuple[str, bool]:
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
        messages = [
            {"role": "system", "content": config.system_prompt},
        ]
        messages += context.get_context(channel_id)
        messages += [{"role": "user", "content": query}]

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
