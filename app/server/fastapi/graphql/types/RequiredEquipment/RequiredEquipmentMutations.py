from typing import Optional

import strawberry
from strawberry.types import Info

from app.server.fastapi.graphql.types.RequiredEquipment.RequiredEquipmentSchema import RequiredEquipmentSchema

@strawberry.mutation
async def create_required_equipment(info: Info, amount: int, item_id: int, discipline_id: int) -> Optional[RequiredEquipmentSchema]:
    return await create_required_equipment(
        amount=amount,
        item_id=item_id,
        discipline_id=discipline_id,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def update_required_equipment(info: Info, id: int, amount: int, item_id: int, discipline_id: int) -> Optional[RequiredEquipmentSchema]:
    return await update_required_equipment(
        id=id,
        amount=amount,
        item_id=item_id,
        discipline_id=discipline_id,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def delete_required_equipment(info: Info, id: int) -> Optional[RequiredEquipmentSchema]:
    return await delete_required_equipment(id=id, user_id=info.context['current_user'].id)
