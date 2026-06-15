from pydantic import BaseModel, Field
from enum import Enum


class DangerType(str, Enum):
    GROOMING = "GROOMING"
    SCAM = "SCAM"
    SEXUAL_CONTENT = "SEXUAL_CONTENT"
    PHISHING = "PHISHING"
    HARASSMENT = "HARASSMENT"
    VIOLENCE = "VIOLENCE"
    UNKNOWN = "UNKNOWN"


class DangerTypeResponseSchema(BaseModel):
    danger_type: DangerType = Field(..., description="The classified type of danger")
    confidence_level: float = Field(..., description="Confidence level 0-100", le=100, ge=0)
    explanation: str = Field(..., description="Brief explanation of why this danger type was identified")
