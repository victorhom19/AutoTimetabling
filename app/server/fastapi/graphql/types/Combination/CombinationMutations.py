from typing import Optional

import strawberry
from strawberry.types import Info

from app.server.fastapi.graphql.types.Combination.CombinationSchema import CombinationSchema

@strawberry.mutation
async def create_combination(info: Info, name: str, project_id: int, color: Optional[str] = None) -> Optional[CombinationSchema]:
    return await create_combination(
        name=name,
        color=color,
        project_id=project_id,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def update_combination(info: Info, id: int, name: str, project_id: int, color: Optional[str] = None) -> Optional[CombinationSchema]:
    return await update_combination(
        id=id,
        name=name,
        color=color,
        project_id=project_id,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def delete_combination(info: Info, id: int) -> Optional[CombinationSchema]:
    return await delete_combination(id=id, user_id=info.context['current_user'].id)
