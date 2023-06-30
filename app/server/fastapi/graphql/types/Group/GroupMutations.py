from typing import Optional

import strawberry
from strawberry.types import Info

from app.server.fastapi.graphql.types.Group.GroupSchema import GroupSchema

@strawberry.mutation
async def create_group(info: Info, code: str, size: int, group_id: int, education_program_id: int, department_id: int) -> Optional[GroupSchema]:
    return await create_group(
        code=code,
        size=size,
        group_id=group_id,
        education_program_id=education_program_id,
        department_id=department_id,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def update_group(info: Info, id: int, code: str, size: int, group_id: int, education_program_id: int, department_id: int) -> Optional[GroupSchema]:
    return await update_group(
        id=id,
        code=code,
        size=size,
        group_id=group_id,
        education_program_id=education_program_id,
        department_id=department_id,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def delete_group(info: Info, id: int) -> Optional[GroupSchema]:
    return await delete_group(id=id, user_id=info.context['current_user'].id)
