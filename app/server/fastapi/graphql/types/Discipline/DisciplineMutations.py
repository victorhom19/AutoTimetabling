from typing import Optional

import strawberry
from strawberry.types import Info

from app.server.fastapi.graphql.types.Discipline.DisciplineSchema import DisciplineSchema

@strawberry.mutation
async def create_discipline(info: Info, name: str, assessment: str, education_module_id: int) -> Optional[DisciplineSchema]:
    return await create_discipline(
        name=name,
        assessment=assessment,
        education_module_id=education_module_id,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def update_discipline(info: Info, id: int, name: str, assessment: str, education_module_id: int) -> Optional[DisciplineSchema]:
    return await update_discipline(
        id=id,
        name=name,
        assessment=assessment,
        education_module_id=education_module_id,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def delete_discipline(info: Info, id: int) -> Optional[DisciplineSchema]:
    return await delete_discipline(id=id, user_id=info.context['current_user'].id)
