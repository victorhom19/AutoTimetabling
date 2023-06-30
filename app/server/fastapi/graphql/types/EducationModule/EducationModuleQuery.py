from typing import Optional, List

import strawberry
from strawberry.exceptions import WrongNumberOfResultsReturned
from strawberry.types import Info

from app.server.fastapi.graphql.types.EducationModule.EducationModuleSchema import EducationModuleSchema, get_all_education_modules

@strawberry.field
async def education_module(info: Info, id: int) -> Optional[EducationModuleSchema]:
    try:
        return await info.context['education_module_loader'].load(id)
    except WrongNumberOfResultsReturned:
        return None

@strawberry.field
async def education_modules(info: Info) -> List[EducationModuleSchema]:
    return await get_all_education_modules(info.context['current_user'].id)
