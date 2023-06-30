from typing import Optional, List

import strawberry
from strawberry.exceptions import WrongNumberOfResultsReturned
from strawberry.types import Info

from app.server.fastapi.graphql.types.Preference.PreferenceSchema import PreferenceSchema, get_all_preferences

@strawberry.field
async def preference(info: Info, id: int) -> Optional[PreferenceSchema]:
    try:
        return await info.context['preference_loader'].load(id)
    except WrongNumberOfResultsReturned:
        return None

@strawberry.field
async def preferences(info: Info, project_id: int) -> List[PreferenceSchema]:
    return await get_all_preferences(project_id, info.context['current_user'].id)
