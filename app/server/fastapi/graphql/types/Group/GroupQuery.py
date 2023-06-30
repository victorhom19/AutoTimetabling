from typing import Optional, List

import strawberry
from strawberry.exceptions import WrongNumberOfResultsReturned
from strawberry.types import Info

from app.server.fastapi.graphql.types.Group.GroupSchema import GroupSchema, get_all_groups

@strawberry.field
async def group(info: Info, id: int) -> Optional[GroupSchema]:
    try:
        return await info.context['group_loader'].load(id)
    except WrongNumberOfResultsReturned:
        return None

@strawberry.field
async def groups(info: Info) -> List[GroupSchema]:
    return await get_all_groups(info.context['current_user'].id)
