from fastapi import APIRouter, HTTPException, status, Query
from src.auth.deps import CurrentUserDep, CurrentUserIdDep, SessionDep
from src.boards.service import BoardsService
from src.boards.schemas import BoardOutputSchema
import uuid


router = APIRouter(prefix="/boards", tags=["Boards"])


# == CREATE NEW BOARD ==
@router.post("/new", response_model=BoardOutputSchema)
async def create_board(
    current_user_id: CurrentUserIdDep,
    session: SessionDep
):
    service = BoardsService(session=session)
    try:
        return await service.create_board(user_id=current_user_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

 
# == DELETE BOARD == 

# == GET ALL BOARDS ==
@router.get("/", response_model=list[BoardOutputSchema])
async def get_boards(
    current_user_id: CurrentUserIdDep,
    session: SessionDep
):
    service = BoardsService(session=session)
    try:
        return await service.get_boards(user_id=current_user_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


# == GET BOARD == (connect to board)

# == SHARE BOARD == 
@router.patch("/{board_id}", response_model=BoardOutputSchema)
async def share_board(
    current_user: CurrentUserIdDep,
    session: SessionDep,
    board_id: uuid.UUID
):
    service = BoardsService(session=session)
    try:
        return await service.share_board(board_id=board_id, user_id=current_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
