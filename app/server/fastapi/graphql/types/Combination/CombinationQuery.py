from typing import Optional, List

import strawberry
from strawberry.exceptions import WrongNumberOfResultsReturned
from strawberry.types import Info

from app.server.fastapi.graphql.types.Combination.CombinationSchema import CombinationSchema, get_all_combinations

@strawberry.field
async def combination(info: Info, id: int) -> Optional[CombinationSchema]:
    try:
        return await info.context['combination_loader'].load(id)
    except WrongNumberOfResultsReturned:
        return None

@strawberry.field
async def combinations(info: Info, project_id: int) -> List[CombinationSchema]:
    return await get_all_combinations(project_id, info.context['current_user'].id)
