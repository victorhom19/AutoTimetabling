from typing import Optional

import strawberry
from strawberry.types import Info

from app.server.fastapi.graphql.types.ClassroomTimeSlot.ClassroomTimeSlotSchema import ClassroomTimeSlotSchema

@strawberry.mutation
async def create_classroom_time_slot(info: Info, amount: int, classroom_id: int, time_slot_id: int) -> Optional[ClassroomTimeSlotSchema]:
    return await create_classroom_time_slot(
        amount=amount,
        classroom_id=classroom_id,
        time_slot_id=time_slot_id,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def update_classroom_time_slot(info: Info, id: int, amount: int, classroom_id: int, time_slot_id: int) -> Optional[ClassroomTimeSlotSchema]:
    return await update_classroom_time_slot(
        id=id,
        amount=amount,
        classroom_id=classroom_id,
        time_slot_id=time_slot_id,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def delete_classroom_time_slot(info: Info, id: int) -> Optional[ClassroomTimeSlotSchema]:
    return await delete_classroom_time_slot(id=id, user_id=info.context['current_user'].id)
