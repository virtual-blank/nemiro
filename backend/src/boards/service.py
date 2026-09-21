from sqlalchemy.ext.asyncio import AsyncSession
from src.boards.repository import BoardsRepository
from src.boards.schemas import BoardOutputSchema
import uuid


class BoardsService:
    def __init__(self, session: AsyncSession):
        self.session=session
        self.repo=BoardsRepository(session=session)
    
    async def create_board(self, user_id: uuid.UUID):
        new_board_dao = await self.repo.create_board(user_id=user_id)
        return BoardOutputSchema.model_validate(new_board_dao)

    async def get_boards(self, user_id: uuid.UUID):
        boards = await self.repo.get_boards(user_id=user_id)
        return [BoardOutputSchema.model_validate(board) for board in boards]
    
    async def share_board(self, user_id: uuid.UUID, board_id: uuid.UUID):
        updated_board_dao = await self.repo.share_board(
            board_id=board_id,
            user_id=user_id
        )
        if not updated_board_dao:
            raise ValueError("Этой доской нельзя поделиться")
        return BoardOutputSchema.model_validate(updated_board_dao)