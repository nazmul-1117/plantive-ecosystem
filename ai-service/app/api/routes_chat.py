from fastapi import APIRouter
from pydantic import BaseModel
from app.services.chat_service import generate_reply

router = APIRouter(
    prefix="/ai/chat",
    tags=["chat"]
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@router.post("/", response_model=ChatResponse)
def chat_with_ai(request: ChatRequest):
    reply = generate_reply(request.message)
    return {"reply": reply}