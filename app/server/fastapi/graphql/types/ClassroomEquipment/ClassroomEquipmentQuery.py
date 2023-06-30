from typing import Optional, List

import strawberry
from strawberry.exceptions import WrongNumberOfResultsReturned
from strawberry.types import Info

from app.server.fastapi.graphql.types.ClassroomEquipment.ClassroomEquipmentSchema import ClassroomEquipmentSchema, get_all_classroom_equipments

@strawberry.field
async def classroom_equipment(info: Info, id: int) -> Optional[ClassroomEquipmentSchema]:
    try:
        return await info.context['classroom_equipment_loader'].load(id)
    except WrongNumberOfResultsReturned:
        return None

@strawberry.field
async def classroom_equipments(info: Info) -> List[ClassroomEquipmentSchema]:
    return await get_all_classroom_equipments(info.context['current_user'].id)
