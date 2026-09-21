from fastapi import APIRouter, HTTPException, status
from src.auth.deps import SessionDep
from src.users.schemas import UserCreateSchema, AuthOutputSchema
from src.users.service import UsersService

router = APIRouter(prefix="/users", tags=["Users"])

# == LOG IN ==
@router.post("/login", response_model=AuthOutputSchema)
async def log_in(
    user_data: UserCreateSchema,
    session: SessionDep
):
    service = UsersService(session=session)
    try:
        return await service.log_in(user_data=user_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


# == SIGN-UP ==
@router.post("/sign-up", response_model=AuthOutputSchema)
async def sign_up(user_data: UserCreateSchema, session: SessionDep):
    service = UsersService(session=session)
    try:
        return await service.sign_up(user_data=user_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
