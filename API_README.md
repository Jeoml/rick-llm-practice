# Rick LLM FastAPI Server

This FastAPI server provides HTTP endpoints to interact with the Rick Sanchez fine-tuned LLM model.

## Quick Start

### 1. Prerequisites
- Ollama installed and running
- Rick LLM model created in Ollama (`ollama create rick-llm -f ollama_files/Modelfile`)

### 2. Install Dependencies
```bash
# Install API dependencies
make install-api-deps

# Or manually:
pip install fastapi httpx uvicorn[standard]
```

### 3. Start the API Server
```bash
# Using the startup script
python start_api.py

# Or using make
make start-api

# Or directly with uvicorn
uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Test the API
```bash
# Run the test script
python test_api.py

# Or using make
make test-api
```

## API Endpoints

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Root Endpoint
- **GET** `/`
- Returns API information and available endpoints

#### 2. Health Check
- **GET** `/health`
- Checks if Ollama is running and the Rick model is available
- Response:
```json
{
  "status": "healthy",
  "model_available": true,
  "model_name": "rick-llm"
}
```

#### 3. Chat
- **POST** `/chat`
- Main endpoint for chatting with Rick
- Request body:
```json
{
  "message": "What's the meaning of life?",
  "conversation_history": [
    {
      "role": "user",
      "content": "Hello Rick"
    },
    {
      "role": "assistant", 
      "content": "Oh, great. Another Morty."
    }
  ]
}
```
- Response:
```json
{
  "response": "The meaning of life? It's simple, Morty. There is no meaning. We're all just cosmic accidents floating through an indifferent universe.",
  "conversation_history": [...]
}
```

#### 4. List Models
- **GET** `/models`
- Lists all available Ollama models

## Interactive API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Example Usage

### Using curl
```bash
# Health check
curl http://localhost:8000/health

# Chat with Rick
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How do I build a portal gun?"}'
```

### Using Python requests
```python
import requests

# Chat with Rick
response = requests.post(
    "http://localhost:8000/chat",
    json={"message": "What's your opinion on Morty?"}
)

print(response.json()["response"])
```

### Using JavaScript fetch
```javascript
const response = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: 'Tell me about interdimensional travel'
  })
});

const data = await response.json();
console.log(data.response);
```

## Configuration

The API server can be configured by modifying the constants in `src/api.py`:

- `OLLAMA_BASE_URL`: Ollama API base URL (default: "http://localhost:11434")
- `MODEL_NAME`: Name of the Rick model in Ollama (default: "rick-llm")

## Troubleshooting

### Common Issues

1. **"Ollama not found" error**
   - Make sure Ollama is running: `ollama serve`
   - Check if the Rick model exists: `ollama list`

2. **"Model not available" error**
   - Create the Rick model: `ollama create rick-llm -f ollama_files/Modelfile`

3. **Connection timeout**
   - The model might be loading for the first time
   - Wait a few minutes and try again

4. **Port already in use**
   - Change the port in `start_api.py` or kill the process using port 8000

### Logs
The API server logs are displayed in the console. For production, consider using a proper logging configuration.

## Production Deployment

For production deployment, consider:

1. **Security**: Configure CORS properly, add authentication
2. **Performance**: Use a production ASGI server like Gunicorn
3. **Monitoring**: Add proper logging and monitoring
4. **Scaling**: Consider load balancing for multiple instances

Example production command:
```bash
gunicorn src.api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

*Wubba lubba dub dub!* 🚀
