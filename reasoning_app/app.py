from __future__ import annotations

import uuid
from typing import Dict, List, Any, AsyncGenerator

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from pydantic import BaseModel

from .llm import get_llm_service


app = FastAPI(title="Reasoning Trainer API")

# In-memory session store; in production use a database or cache.
sessions: Dict[str, Dict[str, Any]] = {}


class StartSessionRequest(BaseModel):
    module: str
    mode: str
    voice: bool = False


class StartSessionResponse(BaseModel):
    session_id: str
    ws_url: str


@app.post("/session/start", response_model=StartSessionResponse)
async def start_session(req: StartSessionRequest) -> StartSessionResponse:
    """Initialize a new interactive reasoning session."""
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        "module": req.module,
        "mode": req.mode,
        "voice": req.voice,
        "messages": [],
    }
    # WebSocket URL relative to the root. The client should connect to this.
    ws_url = f"/ws/{session_id}"
    return StartSessionResponse(session_id=session_id, ws_url=ws_url)


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(ws: WebSocket, session_id: str) -> None:
    """Handle a bidirectional conversation for a session via WebSocket."""
    await ws.accept()
    if session_id not in sessions:
        await ws.close(code=1008)
        return
    llm = get_llm_service()
    try:
        while True:
            data = await ws.receive_json()
            # Expect payload like {"role": "user", "content": "..."}
            role = data.get("role", "user")
            content = data.get("content", "")
            msg = {"role": role, "content": content}
            sessions[session_id]["messages"].append(msg)

            # Ask LLM for a response or next question
            messages = sessions[session_id]["messages"]
            # Generate streaming response
            async for token in llm.stream_complete(messages):
                await ws.send_json({"role": "assistant", "token": token})
    except WebSocketDisconnect:
        # Client disconnected
        return


@app.post("/session/{session_id}/end")
async def end_session(session_id: str) -> Dict[str, Any]:
    """Finalize a session and return summary metrics."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Unknown session")
    history = sessions.pop(session_id)
    # In a full implementation, compute reasoning quality index (RQI) and other metrics.
    return {"session_id": session_id, "messages": history["messages"]}


class AnalyzeRequest(BaseModel):
    text: str


@app.post("/analyze/text")
async def analyze_text(req: AnalyzeRequest) -> Dict[str, Any]:
    """Analyze a block of text for fallacies or rhetorical devices (placeholder)."""
    text = req.text
    # Placeholder: return length and word count
    words = text.split()
    return {"length": len(text), "word_count": len(words)}


@app.get("/progress/summary")
async def progress_summary() -> Dict[str, Any]:
    """Return a simple summary of current sessions (placeholder for progress tracking)."""
    return {"active_sessions": len(sessions)}

