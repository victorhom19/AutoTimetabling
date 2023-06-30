from typing import Optional, List

import strawberry
from strawberry.exceptions import WrongNumberOfResultsReturned
from strawberry.types import Info

from app.server.fastapi.graphql.types.Item.ItemSchema import ItemSchema, get_all_items

@strawberry.field
async def item(info: Info, id: int) -> Optional[ItemSchema]:
    try:
        return await info.context['item_loader'].load(id)
    except WrongNumberOfResultsReturned:
        return None

@strawberry.field
async def items(info: Info) -> List[ItemSchema]:
    return await get_all_items(info.context['current_user'].id)
