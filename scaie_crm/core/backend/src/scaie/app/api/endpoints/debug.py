from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional, cast
from datetime import datetime

from ...core.database import get_db
from ...models.contact import Contact
from ...models.conversation import Conversation, Message

router = APIRouter(prefix="/debug", tags=["debug"])


@router.get("/db-stats")
def db_stats(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Return basic database statistics to verify persistence quickly."""
    contacts = db.query(Contact).count()
    conversations = db.query(Conversation).count()
    messages = db.query(Message).count()

    # Optional: counts by platform (from conversations)
    try:
        from sqlalchemy import func
        by_platform = (
            db.query(Conversation.platform, func.count(Conversation.id))
            .group_by(Conversation.platform)
            .all()
        )
    except Exception:
        by_platform = []

    return {
        "contacts": contacts,
        "conversations": conversations,
        "messages": messages,
        "by_platform": {p or "unknown": c for p, c in by_platform},
    }


@router.get("/recent")
def recent_messages(limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    """Return the most recent messages (agent and user) with minimal context."""
    rows = (
        db.query(Message)
        .order_by(Message.created_at.desc())
        .limit(limit)
        .all()
    )
    result: List[Dict[str, Any]] = []
    # Optionally enrich with contact
    contact_map: Dict[int, str] = {}
    for m in rows:
        name: Optional[str] = None
        cid: Optional[int] = cast(Optional[int], getattr(m, "contact_id", None))
        if cid is not None:
            if cid in contact_map:
                name = contact_map[cid]
            else:
                c = db.query(Contact).filter(Contact.id == cid).first()
                name = cast(Optional[str], c.name) if c else None
                contact_map[cid] = name or ""
        created_at_dt: Optional[datetime] = cast(Optional[datetime], getattr(m, "created_at", None))
        result.append({
            "id": cast(int, getattr(m, "id")),
            "conversation_id": cast(int, getattr(m, "conversation_id")),
            "contact_id": cid,
            "contact_name": name,
            "sender": cast(str, getattr(m, "sender")),
            "content": cast(str, getattr(m, "content")),
            "created_at": created_at_dt.isoformat() if created_at_dt else None,
        })
    return result
