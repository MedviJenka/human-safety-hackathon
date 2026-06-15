from pydantic import BaseModel, Field


class MessageAgentResponseSchema(BaseModel):

    is_safe:          bool = Field(..., description="Whether or not the message is safe.")
    confidence_level: float = Field(..., description="confidence level", le=100, ge=0)
