from fastapi import FastAPI
import uvicorn

# == ROUTERS ==
from src.users.router import router as users_router
from src.boards.router import router as boards_router
# == ROUTERS ==

# == MODELS ==
from src.users.models import User
from src.boards.models import Board, BoardMember
from src.elements.models import Element
# == MODELS ==


ROUTERS_PREFIX = "/api/v1"


app = FastAPI(title="NeMiro", version="0.1")


app.include_router(users_router, prefix=ROUTERS_PREFIX)
app.include_router(boards_router, prefix=ROUTERS_PREFIX)



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True) 