from typing import Optional, List

import strawberry
from strawberry.exceptions import WrongNumberOfResultsReturned
from strawberry.types import Info

from app.server.fastapi.graphql.types.Institution.InstitutionSchema import InstitutionSchema, get_all_institutions

@strawberry.field
async def institution(info: Info, id: int) -> Optional[InstitutionSchema]:
    try:
        return await info.context['institution_loader'].load(id)
    except WrongNumberOfResultsReturned:
        return None

@strawberry.field
async def institutions(info: Info) -> List[InstitutionSchema]:
    return await get_all_institutions(info.context['current_user'].id)
