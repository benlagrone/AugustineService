from pydantic import BaseModel, Field


class Query(BaseModel):
    question: str = Field(..., description="The question to ask")
    mode: str = Field(default="conversation", description="The mode of interaction ('reference' or 'conversation')")
    persona: str = Field(default="Augustine", description="The persona to use (e.g., 'Augustine')")
    session_id: str | None = Field(default=None, description="The session ID for maintaining conversation history")

class TweetResponse(BaseModel):
    tweet: str
    prompt: str
    