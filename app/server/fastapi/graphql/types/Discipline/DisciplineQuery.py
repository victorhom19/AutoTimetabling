from typing import Optional, List

import strawberry
from strawberry.exceptions import WrongNumberOfResultsReturned
from strawberry.types import Info

from app.server.fastapi.graphql.types.Discipline.DisciplineSchema import DisciplineSchema, get_all_disciplines

@strawberry.field
async def discipline(info: Info, id: int) -> Optional[DisciplineSchema]:
    try:
        return await info.context['discipline_loader'].load(id)
    except WrongNumberOfResultsReturned:
        return None

@strawberry.field
async def disciplines(info: Info) -> List[DisciplineSchema]:
    return await get_all_disciplines(info.context['current_user'].id)
