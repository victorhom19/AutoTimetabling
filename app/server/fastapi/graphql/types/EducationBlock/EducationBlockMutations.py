from typing import Optional

import strawberry
from strawberry.types import Info

from app.server.fastapi.graphql.types.EducationBlock.EducationBlockSchema import EducationBlockSchema

@strawberry.mutation
async def create_education_block(info: Info, name: str, code: str, education_program_id: int) -> Optional[EducationBlockSchema]:
    return await create_education_block(
        name=name,
        code=code,
        education_program_id=education_program_id,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def update_education_block(info: Info, id: int, name: str, code: str, education_program_id: int) -> Optional[EducationBlockSchema]:
    return await update_education_block(
        id=id,
        name=name,
        code=code,
        education_program_id=education_program_id,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def delete_education_block(info: Info, id: int) -> Optional[EducationBlockSchema]:
    return await delete_education_block(id=id, user_id=info.context['current_user'].id)
