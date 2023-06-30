from typing import Optional, List

import strawberry
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError
from strawberry.types import Info

from app.server.database.database import async_session_maker
from app.server.database.models import TimeSlot
from app.server.fastapi.graphql.types.User.UserSchema import UserSchema
from app.server.fastapi.graphql.types.Project.ProjectSchema import ProjectSchema


@strawberry.type
class TimeSlotSchema:
    id: int
    
    time_slot_type: str
    week: int
    week_shift: int
    day: int
    class_number:int
    
    user_id: int
    project_id: int
    
    @strawberry.field
    async def user(self, info: Info) -> UserSchema:
        return await info.context['user_loader'].load(self.user_id)

    @strawberry.field
    async def project(self, info: Info) -> ProjectSchema:
        return await info.context['project_loader'].load(self.project_id)

    @staticmethod
    def from_db_instance(db_instance: TimeSlot) -> "TimeSlotSchema":
        return TimeSlotSchema(
            id=db_instance.id,
            time_slot_type=db_instance.time_slot_type,
            week=db_instance.week,
            week_shift=db_instance.week_shift,
            day=db_instance.day,
            class_number=db_instance.class_number,
            user_id=db_instance.user,
            project_id=db_instance.project
        )


async def get_all_time_slots(project_id: Optional[int] = None, user_id: Optional[int] = None) -> List[TimeSlotSchema]:
    async with async_session_maker() as session:
        statement = select(TimeSlot).where(user_id is None or (TimeSlot.project == project_id and TimeSlot.user == user_id))
        db_time_slots = (await session.execute(statement)).scalars().all()

        time_slots = [TimeSlotSchema.from_db_instance(db_time_slot) for db_time_slot in db_time_slots]

        return time_slots


async def create_time_slot(time_slot_type: str, week: int, week_shift: int, day: int, class_number:int, user_id: int, project_id: int) -> Optional[TimeSlotSchema]:
    async with async_session_maker() as session:
        try:
            db_time_slot = TimeSlot(
                time_slot_type=time_slot_type,
                week=week,
                week_shift=week_shift,
                day=day,
                class_number=class_number,
                user=user_id,
                project=project_id
            )
            session.add(db_time_slot)
            await session.commit()
        except IntegrityError:
            return None

        time_slot = TimeSlotSchema.from_db_instance(db_time_slot)

        return time_slot


async def update_time_slot(id: int, time_slot_type: str, week: int, week_shift: int, day: int, class_number:int, user_id: int, project_id: int) -> Optional[TimeSlotSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(TimeSlot).where(TimeSlot.id == id and TimeSlot.user == user_id)
            db_time_slot = (await session.execute(statement)).scalars().one()
            db_time_slot.time_slot_type = time_slot_type
            db_time_slot.week = week
            db_time_slot.week_shift = week_shift
            db_time_slot.day = day
            db_time_slot.class_number = class_number
            db_time_slot.user = user_id
            db_time_slot.project = project_id
            await session.commit()
        except (NoResultFound, IntegrityError):
            return None

        time_slot = TimeSlotSchema.from_db_instance(db_time_slot)

        return time_slot


async def delete_time_slot(id: int, user_id: int) -> Optional[TimeSlotSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(TimeSlot).where(TimeSlot.id == id and TimeSlot.user == user_id)
            db_time_slot = (await session.execute(statement)).scalars().one()
            await session.delete(db_time_slot)
            await session.commit()
        except NoResultFound:
            return None

        time_slot = TimeSlotSchema.from_db_instance(db_time_slot)

        return time_slot
