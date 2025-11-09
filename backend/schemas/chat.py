from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Model for the incoming chat request."""
    user_query: str = Field(..., description="The user's text query to the chatbot.")

class ChatHistoryEntry(BaseModel):
    """Model for a single entry in the chat history database."""
    id: int
    timestamp: str
    user_query: str
    gemini_response: str

class ChatResponse(BaseModel):
    """Model for the response returned by the /chat endpoint."""
    user_query: str
    gemini_response: str
    entry_id: int
