from typing import Optional

import strawberry
from strawberry.types import Info

from app.server.fastapi.graphql.types.Preference.PreferenceSchema import PreferenceSchema

@strawberry.mutation
async def create_preference(info: Info, value: int, project_id: int, lecturer_id: int, time_slot_id: int) -> Optional[PreferenceSchema]:
    return await create_preference(
        value=value,
        project_id=project_id,
        lecturer_id=lecturer_id,
        time_slot_id=time_slot_id,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def update_preference(info: Info, id: int, value: int, project_id: int, lecturer_id: int, time_slot_id: int) -> Optional[PreferenceSchema]:
    return await update_preference(
        id=id,
        value=value,
        project_id=project_id,
        lecturer_id=lecturer_id,
        time_slot_id=time_slot_id,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def delete_preference(info: Info, id: int) -> Optional[PreferenceSchema]:
    return await delete_preference(id=id, user_id=info.context['current_user'].id)
