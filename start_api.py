#!/usr/bin/env python3
"""
Startup script for the Rick LLM FastAPI server.
"""

import uvicorn
import sys
import os

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    print("🚀 Starting Rick LLM API Server...")
    print("📖 API Documentation will be available at: http://localhost:8000/docs")
    print("💬 Chat endpoint: http://localhost:8000/chat")
    print("🏥 Health check: http://localhost:8000/health")
    print("\n*Wubba lubba dub dub!* 🧪")
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )
