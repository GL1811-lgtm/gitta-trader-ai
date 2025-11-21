# backend/agents/shared/message_schema.py
from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Dict, Any, Literal

# Define the allowed message types for better type hinting and validation
MessageType = Literal["strategy", "test_result", "supervisor_summary"]

@dataclass
class AgentMessage:
    """
    A standardized message format for inter-agent communication.
    This ensures that all agents speak the same language.
    """
    message_type: MessageType
    source_agent: str
    payload: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self):
        """Converts the dataclass instance to a dictionary."""
        return {
            "message_type": self.message_type,
            "source_agent": self.source_agent,
            "timestamp": self.timestamp,
            "payload": self.payload,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Creates an AgentMessage instance from a dictionary."""
        return cls(
            message_type=data["message_type"],
            source_agent=data["source_agent"],
            payload=data["payload"],
            timestamp=data.get("timestamp"),
        )
