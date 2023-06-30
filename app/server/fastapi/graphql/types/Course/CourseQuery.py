from typing import Optional, List

import strawberry
from strawberry.exceptions import WrongNumberOfResultsReturned
from strawberry.types import Info

from app.server.fastapi.graphql.types.Course.CourseSchema import CourseSchema, get_all_courses

@strawberry.field
async def course(info: Info, id: int) -> Optional[CourseSchema]:
    try:
        return await info.context['course_loader'].load(id)
    except WrongNumberOfResultsReturned:
        return None

@strawberry.field
async def courses(info: Info, project_id: int) -> List[CourseSchema]:
    return await get_all_courses(project_id, info.context['current_user'].id)
