from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from src.users.repository import UsersRepository
from src.users.schemas import UserCreateSchema, AuthOutputSchema, UserOutputSchema, TokenSchema
from src.auth.hash_argon import create_password, verify_password
from src.auth.security import create_access_token


class UsersService:
    def __init__(self, session: AsyncSession):
        self.session=session
        self.repo=UsersRepository(session=session)
    
    async def sign_up(
        self,
        user_data: UserCreateSchema
    ):
        password = user_data.password_str.get_secret_value()
        password_hash = create_password(password=password)

        try:
            new_user_dao = await self.repo.sign_up(
                username=user_data.username,
                password_hash=password_hash
            )
            token = create_access_token(new_user_dao.id)
            return AuthOutputSchema(
                token = TokenSchema(access_token=token),
                user=UserOutputSchema.model_validate(new_user_dao)
                )

        except IntegrityError as e:
            if "username" in str(e.orig):
                raise ValueError("Этот никнейм уже занят")
        
    async def log_in(self, user_data: UserCreateSchema):
        user_dao = await self.repo.get_user_by_username(username=user_data.username)
        if not user_dao:
            raise ValueError("Не правильный логин или пароль")
        password = user_data.password_str.get_secret_value()
        is_password_correct = verify_password(password=password, hashed_password=user_dao.password_hash)
        if not is_password_correct:
            raise ValueError("Не правильный логин или пароль")
        token = create_access_token(user_dao.id)
        return AuthOutputSchema(
            token=TokenSchema(access_token=token),
            user=UserOutputSchema.model_validate(user_dao)
        )