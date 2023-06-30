from typing import Optional, List

import strawberry
from strawberry.exceptions import WrongNumberOfResultsReturned
from strawberry.types import Info

from app.server.fastapi.graphql.types.EducationProgram.EducationProgramSchema import EducationProgramSchema, get_all_education_programs

@strawberry.field
async def education_program(info: Info, id: int) -> Optional[EducationProgramSchema]:
    try:
        return await info.context['education_program_loader'].load(id)
    except WrongNumberOfResultsReturned:
        return None

@strawberry.field
async def education_programs(info: Info) -> List[EducationProgramSchema]:
    return await get_all_education_programs(info.context['current_user'].id)
