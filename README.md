# Chat Agent

A minimal chat agent starter built with Python and FastAPI.

## Features

- Simple REST API for chat requests
- Optional OpenAI-compatible model integration
- Local fallback response when no API key is configured
- Ready for extension into a web or CLI chat experience

## Quick start

1. Create and activate a virtual environment
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the app:

```bash
uvicorn app:app --reload
```

4. Open the docs:

```text
http://localhost:8000/docs
```

## Example request

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello!","history":[]}'
```

## Environment variables

Set this if you want to use an OpenAI-compatible model:

```bash
export OPENAI_API_KEY=your-key-here
export OPENAI_MODEL=gpt-4o-mini
export OPENAI_BASE_URL=https://api.openai.com/v1
```

The app will fall back to a local mock response if no key is present.
