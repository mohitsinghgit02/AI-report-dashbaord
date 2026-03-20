from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.cache.session_store import get_session
from app.services.groq_chat_stream import stream_chat

router = APIRouter()


class ChatRequest(BaseModel):

    ref_key: str
    question: str


@router.post("/chat/ask")
def chat(req: ChatRequest):

    data = get_session(req.ref_key)

    def generator():

        for chunk in stream_chat(req.question, data):

            yield chunk

    return StreamingResponse(generator(), media_type="text/plain")
