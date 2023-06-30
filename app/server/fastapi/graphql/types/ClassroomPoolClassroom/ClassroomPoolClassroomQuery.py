from typing import Optional, List

import strawberry
from strawberry.exceptions import WrongNumberOfResultsReturned
from strawberry.types import Info

from app.server.fastapi.graphql.types.ClassroomPoolClassroom.ClassroomPoolClassroomSchema import ClassroomPoolClassroomSchema, get_all_classroom_pool_classrooms

@strawberry.field
async def classroom_pool_classroom(info: Info, id: int) -> Optional[ClassroomPoolClassroomSchema]:
    try:
        return await info.context['classroom_pool_classroom_loader'].load(id)
    except WrongNumberOfResultsReturned:
        return None

@strawberry.field
async def classroom_pool_classrooms(info: Info) -> List[ClassroomPoolClassroomSchema]:
    return await get_all_classroom_pool_classrooms(info.context['current_user'].id)
