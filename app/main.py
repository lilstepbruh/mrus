from typing import List
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi import FastAPI
from fastapi.params import Depends
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from schemas import *
from database import *
from crud import *


load_dotenv()
MODEL_API = os.getenv('MODEL_API')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
app = FastAPI()

Base.metadata.create_all(bind=engine)
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

@app.get("/health")
def health():
    return {"status": "ok"}

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=MODEL_API
)

@app.post("/sessions/{session_id}/messages")
async def send_message(session_id: UUID, message_in: MessageCreate, db: Session=Depends(get_db)):

    create_message(
        db=db,
        session_id=session_id,
        role='user',
        content=message_in.content
    )

    history = get_messages_by_session(db=db, session_in=session_id, role='user', limit=5)
    messages = [{'role':msg.role, 'content': msg.content} for msg in history]

    answer = client.chat.completions.create(
        model='z-ai/glm-4.5-air:free',
        messages=messages
    )

    assistant_text = answer.choices[0].message.content

    create_message(
        db=db,
        session_id=session_id,
        role='assistant',
        content=assistant_text
    )

    return {'session_id': session_id,
            'answer': assistant_text}

@app.post("/sessions", response_model=SessionResponse)
def create_new_session(session_in: SessionCreate, db: Session = Depends(get_db)):
    session = create_session(db, session_in)
    return session

@app.get("/sessions/{session_id}/messages", response_model=List[MessageResponse])
def get_messages(session_id: UUID, role: str, db: Session = Depends(get_db)):
    messages = get_messages_by_session(db, session_id, role)
    return messages

@app.get("/sessions")
def read_sessions(db: Session = Depends(get_db)):
    return get_sessions_from_db(db)
