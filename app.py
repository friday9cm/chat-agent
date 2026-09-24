import os
from typing import List, Literal

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

load_dotenv()

app = FastAPI(title="Chat Agent", version="0.1.0")


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    history: List[ChatMessage] = Field(default_factory=list)


class ChatResponse(BaseModel):
    reply: str
    model: str | None = None


def generate_local_reply(message: str, history: List[ChatMessage]) -> str:
    if not message.strip():
        return "I didn't receive a message. Try sending something to chat with me."

    previous = history[-3:]
    context = " ".join(f"{item.role}: {item.content}" for item in previous)
    if context:
        return (
            f"Thanks for the message: '{message}'. "
            f"I can see your recent chat context: {context}. "
            "I am ready to help with questions, planning, and coding tasks."
        )

    return (
        f"Thanks for the message: '{message}'. "
        "I am a simple chat agent and I am ready to help with coding, research, and planning."
    )


def generate_llm_reply(message: str, history: List[ChatMessage]) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return generate_local_reply(message, history)

    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful coding assistant."},
            *[
                {"role": item.role, "content": item.content}
                for item in history
            ],
            {"role": "user", "content": message},
        ],
        "temperature": 0.7,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            f"{base_url.rstrip('/')}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception:
        return generate_local_reply(message, history)


@app.get("/")
def root() -> dict:
    return {"message": "Chat agent is running."}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    reply = generate_llm_reply(request.message, request.history)
    model_name = os.getenv("OPENAI_MODEL") if os.getenv("OPENAI_API_KEY") else None
    return ChatResponse(reply=reply, model=model_name)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
