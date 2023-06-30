import datetime
import json
from typing import List

import uvicorn
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from starlette.middleware.cors import CORSMiddleware

from app.server.database.auth.auth import auth_backend
from app.server.database.auth.schemas import UserRead, UserCreate
from app.server.database.models import User
from app.server.fastapi.dependencies import fastapi_users, current_user, get_async_session
from app.server.fastapi.graphql.index import graphql_app

app = FastAPI()


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


app.include_router(graphql_app, prefix="/graphql")


class UserInfo(BaseModel):
    id: int
    username: str
    email: str


@app.get('/auth/profile', response_model=UserInfo)
async def get_user_info(user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    user = await session.get(User, user.id)
    return UserInfo(id=user.id, username=user.username, email=user.email)



if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=8000)