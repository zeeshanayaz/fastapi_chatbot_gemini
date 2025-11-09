import os
from fastapi import HTTPException
import httpx

async def call_gemini_api(query: str, API_URL: str, API_KEY: str) -> str:
    """
    Calls the Gemini API once without exponential backoff retry logic.
    """
    
    if not API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Gemini API Key is missing. Please set the GEMINI_API_KEY environment variable."
        )

    headers = {'Content-Type': 'application/json'}

    payload = {
        "contents": [{"parts": [{"text": query}]}],
        "systemInstruction": {"parts": [{"text": "You are a helpful and concise chatbot. Keep your responses brief and accurate."}]}
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{API_URL}?key={API_KEY}",
                headers=headers,
                json=payload
            )
            response.raise_for_status() # Raises HTTPStatusError for 4xx/5xx responses

            # Process successful response
            result = response.json()
            text = result['candidates'][0]['content']['parts'][0]['text']
            return text

    except httpx.HTTPStatusError as e:
        # Simple error handling: catch API errors and raise a clear HTTP exception
        print(f"Gemini API HTTP Error: {e.response.status_code}. Detail: {e.response.text.strip()}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Gemini API Error: {e.response.text.strip()}"
        )
    except Exception as e:
        # Catch network or parsing errors
        print(f"An unexpected error occurred during API call: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to communicate with the Gemini API: {e}"
        )
