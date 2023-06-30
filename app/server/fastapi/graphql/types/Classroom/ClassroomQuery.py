from typing import Optional, List

import strawberry
from strawberry.exceptions import WrongNumberOfResultsReturned
from strawberry.types import Info

from app.server.fastapi.graphql.types.Classroom.ClassroomSchema import ClassroomSchema, get_all_classrooms

@strawberry.field
async def classroom(info: Info, id: int) -> Optional[ClassroomSchema]:
    try:
        return await info.context['classroom_loader'].load(id)
    except WrongNumberOfResultsReturned:
        return None

@strawberry.field
async def classrooms(info: Info) -> List[ClassroomSchema]:
    return await get_all_classrooms(info.context['current_user'].id)
