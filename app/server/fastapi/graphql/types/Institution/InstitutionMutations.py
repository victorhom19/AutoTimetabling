from typing import Optional

import strawberry
from strawberry.types import Info

from app.server.fastapi.graphql.types.Institution.InstitutionSchema import InstitutionSchema

@strawberry.mutation
async def create_institution(info: Info, code: str, name: str) -> Optional[InstitutionSchema]:
    return await create_institution(
        code=code,
        name=name,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def update_institution(info: Info, id: int, code: str, name: str) -> Optional[InstitutionSchema]:
    return await update_institution(
        id=id,
        code=code,
        name=name,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def delete_institution(info: Info, id: int) -> Optional[InstitutionSchema]:
    return await delete_institution(id=id, user_id=info.context['current_user'].id)
