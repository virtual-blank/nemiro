from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.users.models import User

class UsersRepository:
    def __init__(self, session: AsyncSession):
        self.session=session
    
    
    async def sign_up(self, username: str, password_hash: str) -> User | None:
        new_user = User(username=username, password_hash=password_hash)

        self.session.add(new_user)
        await self.session.commit()
        return new_user

    async def get_user_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username==username)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    