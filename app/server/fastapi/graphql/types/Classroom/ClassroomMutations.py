from typing import Optional

import strawberry
from strawberry.types import Info

from app.server.fastapi.graphql.types.Classroom.ClassroomSchema import ClassroomSchema

@strawberry.mutation
async def create_classroom(info: Info, building: str, auditory_number: str, capacity: int) -> Optional[ClassroomSchema]:
    return await create_classroom(
        building=building,
        auditory_number=auditory_number,
        capacity=capacity,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def update_classroom(info: Info, id: int, building: str, auditory_number: str, capacity: int) -> Optional[ClassroomSchema]:
    return await update_classroom(
        id=id,
        building=building,
        auditory_number=auditory_number,
        capacity=capacity,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def delete_classroom(info: Info, id: int) -> Optional[ClassroomSchema]:
    return await delete_classroom(id=id, user_id=info.context['current_user'].id)
