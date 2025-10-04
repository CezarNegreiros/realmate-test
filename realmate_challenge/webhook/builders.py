class MessagePayloadBuilder:
    def __init__(
        self,
        timestamp: str,
        message_id: str,
        direction: str,
        content: str,
        conversation_id: str
    ):
        self.timestamp = timestamp
        self.message_id = message_id
        self.direction = direction
        self.content = content
        self.conversation_id = conversation_id

    def build(self) -> dict:
        payload = {
            "type": "NEW_MESSAGE",
            "timestamp": self.timestamp,
            "data": {
                "id": self.message_id,
                "direction": self.direction,
                "content": self.content,
                "conversation_id": self.conversation_id,
            }
        }
        return payload


class ConversationPayloadBuilder:
    def __init__(self, conversation_id: str, timestamp: str):
        self.conversation_id = conversation_id
        self.timestamp = timestamp

    def build(self) -> dict:
        payload = {
            "type": "NEW_CONVERSATION",
            "timestamp": self.timestamp,
            "data": {
                "id": self.conversation_id,
            }
        }

        return payload
