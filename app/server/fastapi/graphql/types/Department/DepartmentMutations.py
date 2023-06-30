from typing import Optional

import strawberry
from strawberry.types import Info

from app.server.fastapi.graphql.types.Department.DepartmentSchema import DepartmentSchema

@strawberry.mutation
async def create_department(info: Info, name: str, institution_id: int) -> Optional[DepartmentSchema]:
    return await create_department(
        name=name,
        institution_id=institution_id,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def update_department(info: Info, id: int, name: str, institution_id: int) -> Optional[DepartmentSchema]:
    return await update_department(
        id=id,
        name=name,
        institution_id=institution_id,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def delete_department(info: Info, id: int) -> Optional[DepartmentSchema]:
    return await delete_department(id=id, user_id=info.context['current_user'].id)
