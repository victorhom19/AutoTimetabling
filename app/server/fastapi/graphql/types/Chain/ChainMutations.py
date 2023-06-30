from typing import Optional

import strawberry
from strawberry.types import Info

from app.server.fastapi.graphql.types.Chain.ChainSchema import ChainSchema

@strawberry.mutation
async def create_chain(info: Info, name: str, project_id: int, color: Optional[str] = None) -> Optional[ChainSchema]:
    return await create_chain(
        name=name,
        color=color,
        project_id=project_id,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def update_chain(info: Info, id: int, name: str, project_id: int, color: Optional[str] = None) -> Optional[ChainSchema]:
    return await update_chain(
        id=id,
        name=name,
        color=color,
        project_id=project_id,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def delete_chain(info: Info, id: int) -> Optional[ChainSchema]:
    return await delete_chain(id=id, user_id=info.context['current_user'].id)
