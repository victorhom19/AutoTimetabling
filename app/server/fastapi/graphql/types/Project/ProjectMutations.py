from typing import Optional

import strawberry
from strawberry.types import Info

from app.server.fastapi.graphql.types.Project.ProjectSchema import ProjectSchema, create_project as create, \
    update_project as update, delete_project as delete


@strawberry.mutation
async def create_project(info: Info, name: str, description: Optional[str] = None) -> Optional[ProjectSchema]:
    return await create(
        name=name,
        description=description,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def update_project(info: Info, id: int, name: str, description: Optional[str] = None) -> Optional[ProjectSchema]:
    return await update(
        id=id,
        name=name,
        description=description,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def delete_project(info: Info, id: int) -> Optional[ProjectSchema]:
    return await delete(id=id, user_id=info.context['current_user'].id)
