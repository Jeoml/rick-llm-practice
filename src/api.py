"""
FastAPI application for serving the Rick LLM via HTTP endpoints.
"""

import asyncio
import json
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Rick LLM API",
    description="API for interacting with the Rick Sanchez fine-tuned LLM",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ollama API configuration
OLLAMA_BASE_URL = "http://localhost:11434"
MODEL_NAME = "rick-llm"

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    response: str
    conversation_history: List[ChatMessage]

class HealthResponse(BaseModel):
    status: str
    model_available: bool
    model_name: str

async def check_ollama_health() -> bool:
    """Check if Ollama service is running and model is available."""
    try:
        async with httpx.AsyncClient() as client:
            # Check if Ollama is running
            response = await client.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5.0)
            if response.status_code != 200:
                return False
            
            # Check if our model is available
            models = response.json().get("models", [])
            model_names = [model.get("name", "") for model in models]
            return any(MODEL_NAME in name for name in model_names)
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return False

async def generate_response(message: str, conversation_history: List[ChatMessage] = None) -> str:
    """Generate a response from the Rick LLM model."""
    if conversation_history is None:
        conversation_history = []
    
    # Prepare the conversation context
    messages = []
    for msg in conversation_history:
        messages.append({"role": msg.role, "content": msg.content})
    
    # Add the current user message
    messages.append({"role": "user", "content": message})
    
    # Prepare the request payload
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.8,
            "min_p": 0.1
        }
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/chat",
                json=payload,
                timeout=60.0
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=500,
                    detail=f"Ollama API error: {response.status_code} - {response.text}"
                )
            
            result = response.json()
            return result.get("message", {}).get("content", "Sorry, I couldn't generate a response.")
            
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Request timeout - model took too long to respond")
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/", response_model=dict)
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Rick LLM API",
        "description": "API for interacting with the Rick Sanchez fine-tuned LLM",
        "endpoints": {
            "chat": "/chat",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    model_available = await check_ollama_health()
    return HealthResponse(
        status="healthy" if model_available else "unhealthy",
        model_available=model_available,
        model_name=MODEL_NAME
    )

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint for interacting with the Rick LLM.
    
    Args:
        request: ChatRequest containing the user message and optional conversation history
        
    Returns:
        ChatResponse with the model's response and updated conversation history
    """
    try:
        # Generate response from the model
        response = await generate_response(request.message, request.conversation_history)
        
        # Update conversation history
        updated_history = request.conversation_history.copy()
        updated_history.append(ChatMessage(role="user", content=request.message))
        updated_history.append(ChatMessage(role="assistant", content=response))
        
        return ChatResponse(
            response=response,
            conversation_history=updated_history
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/models")
async def list_models():
    """List available models."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5.0)
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=500, detail="Failed to fetch models")
    except Exception as e:
        logger.error(f"Error listing models: {e}")
        raise HTTPException(status_code=500, detail="Failed to connect to Ollama")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
