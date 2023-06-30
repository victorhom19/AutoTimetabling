from typing import Optional, List

import strawberry
from strawberry.exceptions import WrongNumberOfResultsReturned
from strawberry.types import Info

from app.server.fastapi.graphql.types.EducationBlock.EducationBlockSchema import EducationBlockSchema, get_all_education_blocks

@strawberry.field
async def education_block(info: Info, id: int) -> Optional[EducationBlockSchema]:
    try:
        return await info.context['education_block_loader'].load(id)
    except WrongNumberOfResultsReturned:
        return None

@strawberry.field
async def education_blocks(info: Info) -> List[EducationBlockSchema]:
    return await get_all_education_blocks(info.context['current_user'].id)
