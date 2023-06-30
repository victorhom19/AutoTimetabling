import strawberry
from strawberry.types import Info

from app.server.fastapi.graphql.types.User.UserSchema import UserSchema


@strawberry.field
async def current_user(info: Info) -> UserSchema:
    user = info.context['current_user']
    return UserSchema(id=user.id, username=user.username, email=user.email)

