#!/usr/bin/env python3
"""
Simple Python script to test the Rick LLM API endpoints.
"""

import requests
import json
import time

API_BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint."""
    print("🏥 Testing health endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health check passed: {health_data}")
            return health_data.get("model_available", False)
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def chat_with_rick(message, conversation_history=None):
    """Send a message to Rick and get his response."""
    if conversation_history is None:
        conversation_history = []
    
    payload = {
        "message": message,
        "conversation_history": conversation_history
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Chat failed: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Chat error: {e}")
        return None

def main():
    """Test the Rick LLM API with various sample messages."""
    print("🧪 Testing Rick LLM API...")
    print("=" * 50)
    
    # Test health first
    if not test_health():
        print("\n❌ Health check failed. Make sure:")
        print("   1. Ollama is running")
        print("   2. Rick model is available")
        print("   3. API server is running")
        return
    
    print("\n💬 Testing chat with Rick...")
    
    # Sample messages to test
    test_messages = [
        "What's the meaning of life?",
        "How do I build a portal gun?",
        "Tell me about interdimensional travel",
        "What's your opinion on Morty?",
        "Can you help me with quantum physics?",
        "What's the best way to deal with existential dread?"
    ]
    
    conversation_history = []
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n--- Test {i} ---")
        print(f"👤 User: {message}")
        
        result = chat_with_rick(message, conversation_history)
        
        if result:
            print(f"🤖 Rick: {result['response']}")
            conversation_history = result['conversation_history']
        else:
            print("❌ Failed to get response")
        
        # Small delay between requests
        time.sleep(1)
    
    print("\n🎉 All tests completed!")
    print(f"\n📖 Try the interactive API docs at: {API_BASE_URL}/docs")

if __name__ == "__main__":
    main()
