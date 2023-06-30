from typing import Optional, List

import strawberry
from strawberry.exceptions import WrongNumberOfResultsReturned
from strawberry.types import Info

from app.server.fastapi.graphql.types.TimeSlot.TimeSlotSchema import TimeSlotSchema, get_all_time_slots

@strawberry.field
async def time_slot(info: Info, id: int) -> Optional[TimeSlotSchema]:
    try:
        return await info.context['time_slot_loader'].load(id)
    except WrongNumberOfResultsReturned:
        return None

@strawberry.field
async def time_slots(info: Info, project_id: int) -> List[TimeSlotSchema]:
    return await get_all_time_slots(project_id, info.context['current_user'].id)
