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
    model_data, base_url, token, client = config.get_model_params(model)
    if model_data == None:
        return (
            f"ERROR: Model '{model}' not found. Make sure you have defined it in 'llmcord.toml'",
            False,
        )

    if client == None:
        return "ERROR: No client has been configured for this model", False

    client = BaseClient.plugins[client]
    response, ok = await client.get_response(
        model_data,
        query,
        base_url,
        token,
        config.system_prompt,
        context.get_context(channel_id),
    )
    return response, ok
