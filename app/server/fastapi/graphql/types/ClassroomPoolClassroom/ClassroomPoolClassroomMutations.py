from typing import Optional

import strawberry
from strawberry.types import Info

from app.server.fastapi.graphql.types.ClassroomPoolClassroom.ClassroomPoolClassroomSchema import ClassroomPoolClassroomSchema

@strawberry.mutation
async def create_classroom_pool_classroom(info: Info, classroom_pool_id: int, classroom_id: int) -> Optional[ClassroomPoolClassroomSchema]:
    return await create_classroom_pool_classroom(
        classroom_pool_id=classroom_pool_id,
        classroom_id=classroom_id,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def update_classroom_pool_classroom(info: Info, id: int, classroom_pool_id: int, classroom_id: int) -> Optional[ClassroomPoolClassroomSchema]:
    return await update_classroom_pool_classroom(
        id=id,
        classroom_pool_id=classroom_pool_id,
        classroom_id=classroom_id,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def delete_classroom_pool_classroom(info: Info, id: int) -> Optional[ClassroomPoolClassroomSchema]:
    return await delete_classroom_pool_classroom(id=id, user_id=info.context['current_user'].id)
