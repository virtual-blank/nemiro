import asyncio
import uuid
from sqlalchemy import update
from database.db import async_session_factory
from src.elements.models import Element
from core.celery_app import celery_app

async def async_update_element(element_id: str, board_id: str, user_id: str, payload: dict):
    element_uuid = uuid.UUID(element_id)
    
    async with async_session_factory() as session:
        # TODO: Добавить проверку прав user_id на редактирование board_id (BoardMember)
        
        stmt = (
            update(Element)
            .where(Element.id == element_uuid, Element.board_id == uuid.UUID(board_id))
            .values(
                x=payload.get("x", Element.x),
                y=payload.get("y", Element.y),
                width=payload.get("width", Element.width),
                height=payload.get("height", Element.height),
                rotation=payload.get("rotation", Element.rotation),
                version=Element.version + 1 
            )
        )
        await session.execute(stmt)
        await session.commit()

@celery_app.task(name="src.elements.tasks.update_element")
def update_element_task(element_id: str, board_id: str, user_id: str, payload: dict):
    asyncio.run(async_update_element(element_id, board_id, user_id, payload))
    return f"Element {element_id} updated"