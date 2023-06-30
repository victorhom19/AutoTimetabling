from typing import Optional, List

import strawberry
from strawberry.exceptions import WrongNumberOfResultsReturned
from strawberry.types import Info

from app.server.fastapi.graphql.types.ClassroomPool.ClassroomPoolSchema import ClassroomPoolSchema, get_all_classroom_pools

@strawberry.field
async def classroom_pool(info: Info, id: int) -> Optional[ClassroomPoolSchema]:
    try:
        return await info.context['classroom_pool_loader'].load(id)
    except WrongNumberOfResultsReturned:
        return None

@strawberry.field
async def classroom_pools(info: Info) -> List[ClassroomPoolSchema]:
    return await get_all_classroom_pools(info.context['current_user'].id)
