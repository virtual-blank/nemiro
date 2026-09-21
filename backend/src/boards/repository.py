from sqlalchemy.ext.asyncio import AsyncSession
from src.boards.models import Board
from sqlalchemy import select, update
import uuid

class BoardsRepository:
    def __init__(self, session: AsyncSession):
        self.session=session
        
    async def create_board(self, user_id: uuid.UUID):
        new_board = Board(owner_id=user_id)
        self.session.add(new_board)
        await self.session.commit()
        return new_board

    async def get_boards(self, user_id: uuid.UUID):
        stmt = select(Board).where(Board.owner_id==user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def share_board(self, user_id: uuid.UUID, board_id: uuid.UUID) -> Board | None:
        stmt = (
            update(Board)
            .where(
                Board.id == board_id,
                Board.owner_id==user_id,
                )
            .values(is_public=True)
            .returning(Board)
        )
        resutl = await self.session.execute(stmt)
        updated_board = resutl.scalar_one_or_none()
        if updated_board:
            await self.session.commit()
        return updated_board