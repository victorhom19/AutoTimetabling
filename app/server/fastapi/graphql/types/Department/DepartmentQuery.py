from typing import Optional, List

import strawberry
from strawberry.exceptions import WrongNumberOfResultsReturned
from strawberry.types import Info

from app.server.fastapi.graphql.types.Department.DepartmentSchema import DepartmentSchema, get_all_departments

@strawberry.field
async def department(info: Info, id: int) -> Optional[DepartmentSchema]:
    try:
        return await info.context['department_loader'].load(id)
    except WrongNumberOfResultsReturned:
        return None

@strawberry.field
async def departments(info: Info) -> List[DepartmentSchema]:
    return await get_all_departments(info.context['current_user'].id)
