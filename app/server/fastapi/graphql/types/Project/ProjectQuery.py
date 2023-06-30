from typing import Optional, List

import strawberry
from strawberry.exceptions import WrongNumberOfResultsReturned
from strawberry.types import Info

from app.server.fastapi.graphql.types.Project.ProjectSchema import ProjectSchema, get_all_projects

@strawberry.field
async def project(info: Info, id: int) -> Optional[ProjectSchema]:
    try:
        return await info.context['project_loader'].load(id)
    except WrongNumberOfResultsReturned:
        return None

@strawberry.field
async def projects(info: Info) -> List[ProjectSchema]:
    return await get_all_projects(info.context['current_user'].id)
