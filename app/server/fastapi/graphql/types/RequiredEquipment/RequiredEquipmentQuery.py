from typing import Optional, List

import strawberry
from strawberry.exceptions import WrongNumberOfResultsReturned
from strawberry.types import Info

from app.server.fastapi.graphql.types.RequiredEquipment.RequiredEquipmentSchema import RequiredEquipmentSchema, get_all_required_equipments

@strawberry.field
async def required_equipment(info: Info, id: int) -> Optional[RequiredEquipmentSchema]:
    try:
        return await info.context['required_equipment_loader'].load(id)
    except WrongNumberOfResultsReturned:
        return None

@strawberry.field
async def required_equipments(info: Info) -> List[RequiredEquipmentSchema]:
    return await get_all_required_equipments(info.context['current_user'].id)
