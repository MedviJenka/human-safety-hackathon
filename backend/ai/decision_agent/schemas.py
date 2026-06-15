from pydantic import BaseModel, Field
from enum import Enum


class AlertLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class TargetUserType(str, Enum):
    CHILD = "CHILD"
    ADULT = "ADULT"
    UNKNOWN = "UNKNOWN"


class SafetyReportSchema(BaseModel):
    alert_level: AlertLevel = Field(..., description="Severity of the threat")
    danger_type: str = Field(..., description="Classified danger type")
    summary: str = Field(..., description="Human-readable summary for a parent or guardian")
    recommended_action: str = Field(..., description="Clear next step the guardian or platform should take")
    evidence_snippets: list[str] = Field(..., description="Exact phrases from the message that triggered the alert")
    target_user_type: TargetUserType = Field(..., description="Who appears to be at risk")
    should_notify_guardian: bool = Field(..., description="Send immediate notification to guardian")
    should_block_sender: bool = Field(..., description="Block the sender immediately")
