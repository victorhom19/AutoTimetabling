from typing import Optional

import strawberry
from strawberry.types import Info

from app.server.fastapi.graphql.types.ClassroomPool.ClassroomPoolSchema import ClassroomPoolSchema

@strawberry.mutation
async def create_classroom_pool(info: Info, name: str, color: Optional[str] = None) -> Optional[ClassroomPoolSchema]:
    return await create_classroom_pool(
        name=name,
        color=color,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def update_classroom_pool(info: Info, id: int, name: str, color: Optional[str] = None) -> Optional[ClassroomPoolSchema]:
    return await update_classroom_pool(
        id=id,
        name=name,
        color=color,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def delete_classroom_pool(info: Info, id: int) -> Optional[ClassroomPoolSchema]:
    return await delete_classroom_pool(id=id, user_id=info.context['current_user'].id)
