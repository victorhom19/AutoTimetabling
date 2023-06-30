from typing import List

import strawberry
from sqlalchemy import select

from app.server.database.database import async_session_maker
from app.server.database.models import User


@strawberry.type
class UserSchema:
    id: int
    username: str
    email: str


async def get_all_users() -> List["UserSchema"]:
    async with async_session_maker() as session:
        db_users = (await session.execute(select(User))).scalars().all()

        users = [
            UserSchema(
                id=db_user.id,
                username=db_user.username,
                email=db_user.email
            )
            for db_user in db_users
        ]

        return users
