from typing import Optional, List

import strawberry
from strawberry.exceptions import WrongNumberOfResultsReturned
from strawberry.types import Info

from app.server.fastapi.graphql.types.Lecturer.LecturerSchema import LecturerSchema, get_all_lecturers

@strawberry.field
async def lecturer(info: Info, id: int) -> Optional[LecturerSchema]:
    try:
        return await info.context['lecturer_loader'].load(id)
    except WrongNumberOfResultsReturned:
        return None

@strawberry.field
async def lecturers(info: Info) -> List[LecturerSchema]:
    return await get_all_lecturers(info.context['current_user'].id)
