from typing import Optional

import strawberry
from strawberry.types import Info

from app.server.fastapi.graphql.types.Lecturer.LecturerSchema import LecturerSchema

@strawberry.mutation
async def create_lecturer(info: Info, name: str, department_id: int, email: Optional[str] = None) -> Optional[LecturerSchema]:
    return await create_lecturer(
        name=name,
        email=email,
        department_id=department_id,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def update_lecturer(info: Info, id: int, name: str, department_id: int, email: Optional[str] = None) -> Optional[LecturerSchema]:
    return await update_lecturer(
        id=id,
        name=name,
        email=email,
        department_id=department_id,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def delete_lecturer(info: Info, id: int) -> Optional[LecturerSchema]:
    return await delete_lecturer(id=id, user_id=info.context['current_user'].id)
