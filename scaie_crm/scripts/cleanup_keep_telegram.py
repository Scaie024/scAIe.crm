#!/usr/bin/env python3
import os
import sys
from typing import List

# Ensure backend src is in path
ROOT = os.path.dirname(os.path.dirname(__file__))
BACKEND_SRC = os.path.join(ROOT, 'backend', 'src')
sys.path.append(BACKEND_SRC)

from scaie.app.core.database import SessionLocal  # type: ignore
from scaie.app.models.conversation import Conversation, Message  # type: ignore
from scaie.app.models.agent_action import AgentAction, AgentTask  # type: ignore
from scaie.app.models.contact import Contact, PlatformType  # type: ignore
from sqlalchemy import and_, func


def cleanup_keep_telegram():
    db = SessionLocal()
    try:
        # Counts before
        total_contacts = db.query(Contact).count()
        total_convs = db.query(Conversation).count()
        total_msgs = db.query(Message).count()
        by_platform = dict(db.query(Conversation.platform, func.count(Conversation.id)).group_by(Conversation.platform))
        print(f"Before → contacts={total_contacts}, conversations={total_convs}, messages={total_msgs}, by_platform={by_platform}")

        # 1) Delete all non-telegram conversations (and their messages and actions)
        non_tg_convs: List[int] = [cid for (cid,) in db.query(Conversation.id).filter(Conversation.platform != 'telegram').all()]
        if non_tg_convs:
            # Delete dependent rows first
            db.query(Message).filter(Message.conversation_id.in_(non_tg_convs)).delete(synchronize_session=False)
            db.query(AgentAction).filter(AgentAction.conversation_id.in_(non_tg_convs)).delete(synchronize_session=False)
            # Then conversations
            db.query(Conversation).filter(Conversation.id.in_(non_tg_convs)).delete(synchronize_session=False)
            db.commit()

        # 2) Remove contacts that have no remaining conversations and have no telegram_user_id
        contacts_to_delete: List[int] = []
        for c in db.query(Contact).all():
            has_convs = db.query(Conversation.id).filter(Conversation.contact_id == c.id).first() is not None
            if not has_convs and not getattr(c, 'telegram_user_id', None):
                contacts_to_delete.append(c.id)
        if contacts_to_delete:
            # Delete tasks linked to these contacts first
            db.query(AgentTask).filter(AgentTask.contact_id.in_(contacts_to_delete)).delete(synchronize_session=False)
            db.query(Contact).filter(Contact.id.in_(contacts_to_delete)).delete(synchronize_session=False)
            db.commit()

        # 3) Normalize contact.platform to TELEGRAM if they only have telegram conversations
        for c in db.query(Contact).all():
            has_tg_conv = db.query(Conversation.id).filter(and_(Conversation.contact_id == c.id, Conversation.platform == 'telegram')).first() is not None
            if has_tg_conv and getattr(c, 'platform', None) != PlatformType.TELEGRAM:
                try:
                    c.platform = PlatformType.TELEGRAM
                except Exception:
                    pass
        db.commit()

        # Counts after
        total_contacts = db.query(Contact).count()
        total_convs = db.query(Conversation).count()
        total_msgs = db.query(Message).count()
        by_platform = dict(db.query(Conversation.platform, func.count(Conversation.id)).group_by(Conversation.platform))
        print(f"After  → contacts={total_contacts}, conversations={total_convs}, messages={total_msgs}, by_platform={by_platform}")

    finally:
        db.close()


if __name__ == '__main__':
    cleanup_keep_telegram()
