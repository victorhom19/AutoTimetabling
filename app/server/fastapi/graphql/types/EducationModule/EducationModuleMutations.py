from typing import Optional

import strawberry
from strawberry.types import Info

from app.server.fastapi.graphql.types.EducationModule.EducationModuleSchema import EducationModuleSchema

@strawberry.mutation
async def create_education_module(info: Info, name: str, code: str, is_base_module: bool, education_module_id: int, education_block_id: int) -> Optional[EducationModuleSchema]:
    return await create_education_module(
        name=name,
        code=code,
        is_base_module=is_base_module,
        education_module_id=education_module_id,
        education_block_id=education_block_id,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def update_education_module(info: Info, id: int, name: str, code: str, is_base_module: bool, education_module_id: int, education_block_id: int) -> Optional[EducationModuleSchema]:
    return await update_education_module(
        id=id,
        name=name,
        code=code,
        is_base_module=is_base_module,
        education_module_id=education_module_id,
        education_block_id=education_block_id,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def delete_education_module(info: Info, id: int) -> Optional[EducationModuleSchema]:
    return await delete_education_module(id=id, user_id=info.context['current_user'].id)
