import pickle
import os

CONTEXT_FILE = "context.pkl"


class Context:
    def __init__(self) -> None:
        if not os.path.exists(CONTEXT_FILE) or os.path.getsize(CONTEXT_FILE) == 0:
            self.context = {}
        else:
            with open(CONTEXT_FILE, "rb") as f:
                self.context = pickle.load(f)

    def add_context_message(self, message: str, role: str, channel_id: str):
        if channel_id not in self.context.keys():
            self.context[channel_id] = [{"role": role, "content": message}]
            return

        self.context[channel_id].append({"role": role, "content": message})

        with open(CONTEXT_FILE, "wb") as f:
            pickle.dump(self.context, f)

    def get_context(self, channel_id: str) -> list[dict]:
        if channel_id not in self.context.keys():
            return []
        return self.context[channel_id]

    def clear(self, channel_id: str):
        self.context[channel_id] = []
        with open(CONTEXT_FILE, "wb") as f:
            pickle.dump(self.context, f)
