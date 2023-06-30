from typing import Optional, List

import strawberry
from strawberry.exceptions import WrongNumberOfResultsReturned
from strawberry.types import Info

from app.server.fastapi.graphql.types.Chain.ChainSchema import ChainSchema, get_all_chains

@strawberry.field
async def chain(info: Info, id: int) -> Optional[ChainSchema]:
    try:
        return await info.context['chain_loader'].load(id)
    except WrongNumberOfResultsReturned:
        return None

@strawberry.field
async def chains(info: Info, project_id: int) -> List[ChainSchema]:
    return await get_all_chains(project_id, info.context['current_user'].id)
