from typing import Optional

import strawberry
from strawberry.types import Info

from app.server.fastapi.graphql.types.TimeSlot.TimeSlotSchema import TimeSlotSchema

@strawberry.mutation
async def create_time_slot(info: Info, time_slot_type: str, week: int, week_shift: int, day: int, class_number:int, project_id: int) -> Optional[TimeSlotSchema]:
    return await create_time_slot(
        time_slot_type=time_slot_type,
        week=week,
        week_shift=week_shift,
        day=day,
        class_number=class_number,
        project_id=project_id,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def update_time_slot(info: Info, id: int, time_slot_type: str, week: int, week_shift: int, day: int, class_number:int, project_id: int) -> Optional[TimeSlotSchema]:
    return await update_time_slot(
        id=id,
        time_slot_type=time_slot_type,
        week=week,
        week_shift=week_shift,
        day=day,
        class_number=class_number,
        project_id=project_id,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def delete_time_slot(info: Info, id: int) -> Optional[TimeSlotSchema]:
    return await delete_time_slot(id=id, user_id=info.context['current_user'].id)
