from typing import Optional

import strawberry
from strawberry.types import Info

from app.server.fastapi.graphql.types.ClassroomEquipment.ClassroomEquipmentSchema import ClassroomEquipmentSchema

@strawberry.mutation
async def create_classroom_equipment(info: Info, amount: int, item_id: int, classroom_id: int) -> Optional[ClassroomEquipmentSchema]:
    return await create_classroom_equipment(
        amount=amount,
        item_id=item_id,
        classroom_id=classroom_id,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def update_classroom_equipment(info: Info, id: int, amount: int, item_id: int, classroom_id: int) -> Optional[ClassroomEquipmentSchema]:
    return await update_classroom_equipment(
        id=id,
        amount=amount,
        item_id=item_id,
        classroom_id=classroom_id,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def delete_classroom_equipment(info: Info, id: int) -> Optional[ClassroomEquipmentSchema]:
    return await delete_classroom_equipment(id=id, user_id=info.context['current_user'].id)
