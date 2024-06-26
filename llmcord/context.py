"""LLMCord"""

import pickle
import os
import logging

CONTEXT_FILE = "context.pkl"


class ContextError(Exception):
    """Represents an error that can occur while loading the context"""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class Context:
    """
    Represents a context manager for storing and retrieving context messages.

    Attributes:
        context (dict): A dictionary that stores the context messages.
    """

    def __init__(self) -> None:
        """
        Initializes the Context object.

        If the context file does not exist or is empty, an empty dictionary is created.
        Otherwise, the context is loaded from the file.
        """
        if not os.path.exists(CONTEXT_FILE) or os.path.getsize(CONTEXT_FILE) == 0:
            self.context = {}
            logging.getLogger("llmcord").info("Created context")
        else:
            with open(CONTEXT_FILE, "rb") as f:
                self.context = pickle.load(f)
                logging.getLogger("llmcord").info("Loaded context")

    def add_context_message(self, message: str, role: str, channel_id: str):
        """
        Adds a context message to the specified channel.

        Args:
            message (str): The content of the context message.
            role (str): The role associated with the context message. Either user or assistant
            channel_id (str): The ID of the channel where the context message is added.
        """
        if role.lower() not in ["user", "assistant"]:
            raise ContextError("Invalid role. Must be 'user' or 'assistant'")

        if channel_id not in self.context.keys():
            self.context[channel_id] = [{"role": role, "content": message}]
            return

        self.context[channel_id].append({"role": role, "content": message})

        with open(CONTEXT_FILE, "wb") as f:
            pickle.dump(self.context, f)

    def get_context(self, channel_id: str) -> list[dict]:
        """
        Retrieves the context messages for the specified channel.

        Args:
            channel_id (str): The ID of the channel.

        Returns:
            list[dict]: A list of dictionaries representing the context messages.
        """
        return self.context.get(channel_id, [])

    def clear(self, channel_id: str):
        """
        Clears the context messages for the specified channel.

        Args:
            channel_id (str): The ID of the channel.
        """
        self.context[channel_id] = []
        with open(CONTEXT_FILE, "wb") as f:
            pickle.dump(self.context, f)
