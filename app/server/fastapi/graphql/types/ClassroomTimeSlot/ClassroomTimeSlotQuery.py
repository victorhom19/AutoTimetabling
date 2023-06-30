from typing import Optional, List

import strawberry
from strawberry.exceptions import WrongNumberOfResultsReturned
from strawberry.types import Info

from app.server.fastapi.graphql.types.ClassroomTimeSlot.ClassroomTimeSlotSchema import ClassroomTimeSlotSchema, get_all_classroom_time_slots

@strawberry.field
async def classroom_time_slot(info: Info, id: int) -> Optional[ClassroomTimeSlotSchema]:
    try:
        return await info.context['classroom_time_slot_loader'].load(id)
    except WrongNumberOfResultsReturned:
        return None

@strawberry.field
async def classroom_time_slots(info: Info) -> List[ClassroomTimeSlotSchema]:
    return await get_all_classroom_time_slots(info.context['current_user'].id)
