from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from ...services.chat_model import ChatModel
from ...core.config import settings

router = APIRouter()
chat_model = ChatModel()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    max_tokens: Optional[int] = 512

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # 获取最后一条用户消息
        user_message = next((msg.content for msg in reversed(request.messages) 
                           if msg.role == "user"), None)
        if not user_message:
            raise HTTPException(status_code=400, detail="No user message found")

        # 格式化历史消息
        chat_history = [{"role": msg.role, "content": msg.content} 
                       for msg in request.messages[:-1]]

        # 格式化提示词
        prompt = chat_model.format_prompt(user_message, chat_history)

        # 生成回复
        response = chat_model.generate_response(
            prompt, 
            max_new_tokens=request.max_tokens
        )

        return ChatResponse(response=response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 