import os
from typing import List
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

from backend.database.database import fetch_all_history, init_database, save_chat_entry
from backend.schemas.chat import ChatHistoryEntry, ChatResponse, ChatRequest
from backend.gemini.gemini import call_gemini_api

load_dotenv(dotenv_path='../.env.local')

API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyD_-Y_cqi8IXPQcjln3RUjrvdjje5zmItY")
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent"


app = FastAPI(
    title='Chatbot using Gemini and FastAPI',
    description='A FastAPI application that integrates with Gemini for chatbot functionalities.',
    version='0.0.1'
)

@app.on_event('startup')
async def startup_event():
    await init_database()
    if not API_KEY:
        print("WARNING: GEMINI_API_KEY is not set in environment variables!")


@app.get('/')
def health_check():
    return {
        'status': True,
        'message': 'API is running successfully.'
    }


# Retrieves all stored chat history entries
@app.get("/history", response_model=List[ChatHistoryEntry])
async def get_chat_history():
    history = await fetch_all_history()
    return history


@app.post("/chat", response_model=ChatResponse)
async def chat_with_gemini(request: ChatRequest):
    try:
        user_query_id = await save_chat_entry(request.user_query, "")

        gemini_response = await call_gemini_api(request.user_query, API_URL, API_KEY)

        gemini_response_id = await save_chat_entry(request.user_query, gemini_response)

        return ChatResponse(
            user_query=request.user_query,
            gemini_response=gemini_response,
            entry_id=gemini_response_id
        )


    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")