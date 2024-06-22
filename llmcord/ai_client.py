from plugins import BaseClient
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
    model, base_url, token, client = config.get_model_params(model)
    # Default to OpenAI client if none was defined
    if client == None:
        response, ok = await BaseClient.plugins["OpenAIClient"].get_response(
            model,
            query,
            base_url,
            token,
            config.system_prompt,
            context.get_context(channel_id),
        )
        return response, ok

    client = BaseClient.plugins[client]
    response, ok = await client.get_response(
        model,
        query,
        base_url,
        token,
        config.system_prompt,
        context.get_context(channel_id),
    )
    return response, ok
