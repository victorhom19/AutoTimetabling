from typing import Optional

import strawberry
from strawberry.types import Info

from app.server.fastapi.graphql.types.EducationProgram.EducationProgramSchema import EducationProgramSchema, \
    create_education_program as create, update_education_program as update, delete_education_program as delete

@strawberry.mutation
async def create_education_program(info: Info, name: str, code: str, profile_name: str, profile_code: str, education_level: str) -> Optional[EducationProgramSchema]:
    return await create(
        name=name,
        code=code,
        profile_name=profile_name,
        profile_code=profile_code,
        education_level=education_level,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def update_education_program(info: Info, id: int, name: str, code: str, profile_name: str, profile_code: str, education_level: str) -> Optional[EducationProgramSchema]:
    return await update(
        id=id,
        name=name,
        code=code,
        profile_name=profile_name,
        profile_code=profile_code,
        education_level=education_level,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def delete_education_program(info: Info, id: int) -> Optional[EducationProgramSchema]:
    return await delete(id=id, user_id=info.context['current_user'].id)
