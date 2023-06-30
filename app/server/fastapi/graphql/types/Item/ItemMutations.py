from typing import Optional

import strawberry
from strawberry.types import Info

from app.server.fastapi.graphql.types.Item.ItemSchema import ItemSchema

@strawberry.mutation
async def create_item(info: Info, name: str, description: Optional[str] = None) -> Optional[ItemSchema]:
    return await create_item(
        name=name,
        description=description,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def update_item(info: Info, id: int, name: str, description: Optional[str] = None) -> Optional[ItemSchema]:
    return await update_item(
        id=id,
        name=name,
        description=description,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def delete_item(info: Info, id: int) -> Optional[ItemSchema]:
    return await delete_item(id=id, user_id=info.context['current_user'].id)
