#!/usr/bin/env python3
"""
Test script for the Rick LLM API.
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

def test_chat():
    """Test the chat endpoint."""
    print("\n💬 Testing chat endpoint...")
    
    # Test message
    test_message = "What's the meaning of life?"
    
    payload = {
        "message": test_message,
        "conversation_history": []
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            chat_data = response.json()
            print(f"✅ Chat test passed!")
            print(f"📝 User: {test_message}")
            print(f"🤖 Rick: {chat_data['response']}")
            return True
        else:
            print(f"❌ Chat test failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Chat test error: {e}")
        return False

def test_models():
    """Test the models endpoint."""
    print("\n📋 Testing models endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/models")
        if response.status_code == 200:
            models_data = response.json()
            print(f"✅ Models endpoint working: {len(models_data.get('models', []))} models found")
            return True
        else:
            print(f"❌ Models endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Models endpoint error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Rick LLM API...")
    print("=" * 50)
    
    # Wait a moment for the server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)
    
    # Test health first
    if not test_health():
        print("\n❌ Health check failed. Make sure:")
        print("   1. Ollama is running (ollama serve)")
        print("   2. Rick model is available (ollama list)")
        print("   3. API server is running (python start_api.py)")
        return
    
    # Test other endpoints
    test_models()
    test_chat()
    
    print("\n🎉 All tests completed!")
    print("\n📖 Try the interactive API docs at: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
