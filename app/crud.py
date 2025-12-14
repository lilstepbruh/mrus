from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.sql.visitors import replacement_traverse

from models import Message
from models import Session as SessionModel
from schemas import SessionCreate

def create_session(db: Session, session_in: SessionCreate):
    new_sess = SessionModel(name=session_in.name)
    db.add(new_sess)
    db.commit()
    db.refresh(new_sess)
    return new_sess

def create_message(db: Session, session_id, role: str, content: str):
    msg = Message(session_id=session_id, role=role, content=content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

def get_messages_by_session(db: Session, session_in: UUID, role: str, limit: int | None = None):
    query = (
        db.query(Message)
        .filter(Message.session_id == session_in)
        .filter(Message.role == role)
        .order_by(Message.created_at.asc())
    )

    if limit:
        query = query.limit(limit)

    return query.all()

def get_sessions_from_db(db: SessionModel, limit: int | None = None):
    query = db.query(SessionModel).order_by(SessionModel.created_at.asc())

    if limit:
        query = query.limit(limit)

    return query.all()

