from typing import Optional

import strawberry
from strawberry.types import Info

from app.server.fastapi.graphql.types.Course.CourseSchema import CourseSchema

@strawberry.mutation
async def create_course(info: Info, course_type: str, duration: int, week_intensity: int, block_length: int, project_id: int, discipline_id: int, lecturer_id: int, group_id: int, combination_id: int, chain_id: int, time_slot_id: int, classroom_pool_id: int, chain_priority: Optional[int] = None) -> Optional[CourseSchema]:
    return await create_course(
        course_type=course_type,
        duration=duration,
        week_intensity=week_intensity,
        block_length=block_length,
        chain_priority=chain_priority,
        project_id=project_id,
        discipline_id=discipline_id,
        lecturer_id=lecturer_id,
        group_id=group_id,
        combination_id=combination_id,
        chain_id=chain_id,
        time_slot_id=time_slot_id,
        classroom_pool_id=classroom_pool_id,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def update_course(info: Info, id: int, course_type: str, duration: int, week_intensity: int, block_length: int, project_id: int, discipline_id: int, lecturer_id: int, group_id: int, combination_id: int, chain_id: int, time_slot_id: int, classroom_pool_id: int, chain_priority: Optional[int] = None) -> Optional[CourseSchema]:
    return await update_course(
        id=id,
        course_type=course_type,
        duration=duration,
        week_intensity=week_intensity,
        block_length=block_length,
        chain_priority=chain_priority,
        project_id=project_id,
        discipline_id=discipline_id,
        lecturer_id=lecturer_id,
        group_id=group_id,
        combination_id=combination_id,
        chain_id=chain_id,
        time_slot_id=time_slot_id,
        classroom_pool_id=classroom_pool_id,
        user_id=info.context['current_user'].id
    )

@strawberry.mutation
async def delete_course(info: Info, id: int) -> Optional[CourseSchema]:
    return await delete_course(id=id, user_id=info.context['current_user'].id)
