from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional
import uuid

@dataclass
class Message:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sender: str = ""
    receiver: str = ""
    subject: str = ""
    content: str = ""
    request_id: Optional[str] = None
    reply_to: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)

class MessageBus:
    def __init__(self):
        self.messages: Dict[str, Message] = {}
        self.inboxes: Dict[str, list] = {}
    
    def send_message(self, message: Message) -> str:
        self.messages[message.id] = message
        if message.receiver not in self.inboxes:
            self.inboxes[message.receiver] = []
        self.inboxes[message.receiver].append(message.id)
        return message.id
    
    def get_inbox(self, agent_type: str) -> list:
        if agent_type not in self.inboxes:
            return []
        return [self.messages[mid] for mid in self.inboxes[agent_type]]
