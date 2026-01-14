from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from src.api.dependencies import get_rag_chain

router = APIRouter()

@router.get("/rag/stream")
async def stream_rag(question: str):
    chain = get_rag_chain()

    async def token_stream():
        async for chunk in chain.astream(question):
            yield f"data: {chunk}\n\n"

    return StreamingResponse(
        token_stream(),
        media_type="text/event-stream",
    )