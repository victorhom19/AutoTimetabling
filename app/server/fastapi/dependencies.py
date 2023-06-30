from collections import AsyncGenerator

from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession

from app.server.database.auth.auth import auth_backend
from app.server.database.auth.manager import get_user_manager
from app.server.database.database import async_session_maker
from app.server.database.models import User

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

current_user = fastapi_users.current_user()