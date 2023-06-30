from typing import Optional, List

import strawberry
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError
from strawberry.types import Info

from app.server.database.database import async_session_maker
from app.server.database.models import ClassroomTimeSlot
from app.server.fastapi.graphql.types.User.UserSchema import UserSchema
from app.server.fastapi.graphql.types.Classroom.ClassroomSchema import ClassroomSchema
from app.server.fastapi.graphql.types.TimeSlot.TimeSlotSchema import TimeSlotSchema


@strawberry.type
class ClassroomTimeSlotSchema:
    id: int
    
    amount: int
    
    user_id: int
    classroom_id: int
    time_slot_id: int
    
    @strawberry.field
    async def user(self, info: Info) -> UserSchema:
        return await info.context['user_loader'].load(self.user_id)

    @strawberry.field
    async def classroom(self, info: Info) -> ClassroomSchema:
        return await info.context['classroom_loader'].load(self.classroom_id)

    @strawberry.field
    async def time_slot(self, info: Info) -> TimeSlotSchema:
        return await info.context['time_slot_loader'].load(self.time_slot_id)

    @staticmethod
    def from_db_instance(db_instance: ClassroomTimeSlot) -> "ClassroomTimeSlotSchema":
        return ClassroomTimeSlotSchema(
            id=db_instance.id,
            amount=db_instance.amount,
            user_id=db_instance.user,
            classroom_id=db_instance.classroom,
            time_slot_id=db_instance.time_slot
        )


async def get_all_classroom_time_slots(user_id: Optional[int] = None) -> List[ClassroomTimeSlotSchema]:
    async with async_session_maker() as session:
        statement = select(ClassroomTimeSlot).where(user_id is None or ClassroomTimeSlot.user == user_id)
        db_classroom_time_slots = (await session.execute(statement)).scalars().all()

        classroom_time_slots = [ClassroomTimeSlotSchema.from_db_instance(db_classroom_time_slot) for db_classroom_time_slot in db_classroom_time_slots]

        return classroom_time_slots


async def create_classroom_time_slot(amount: int, user_id: int, classroom_id: int, time_slot_id: int) -> Optional[ClassroomTimeSlotSchema]:
    async with async_session_maker() as session:
        try:
            db_classroom_time_slot = ClassroomTimeSlot(
                amount=amount,
                user=user_id,
                classroom=classroom_id,
                time_slot=time_slot_id
            )
            session.add(db_classroom_time_slot)
            await session.commit()
        except IntegrityError:
            return None

        classroom_time_slot = ClassroomTimeSlotSchema.from_db_instance(db_classroom_time_slot)

        return classroom_time_slot


async def update_classroom_time_slot(id: int, amount: int, user_id: int, classroom_id: int, time_slot_id: int) -> Optional[ClassroomTimeSlotSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(ClassroomTimeSlot).where(ClassroomTimeSlot.id == id and ClassroomTimeSlot.user == user_id)
            db_classroom_time_slot = (await session.execute(statement)).scalars().one()
            db_classroom_time_slot.amount = amount
            db_classroom_time_slot.user = user_id
            db_classroom_time_slot.classroom = classroom_id
            db_classroom_time_slot.time_slot = time_slot_id
            await session.commit()
        except (NoResultFound, IntegrityError):
            return None

        classroom_time_slot = ClassroomTimeSlotSchema.from_db_instance(db_classroom_time_slot)

        return classroom_time_slot


async def delete_classroom_time_slot(id: int, user_id: int) -> Optional[ClassroomTimeSlotSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(ClassroomTimeSlot).where(ClassroomTimeSlot.id == id and ClassroomTimeSlot.user == user_id)
            db_classroom_time_slot = (await session.execute(statement)).scalars().one()
            await session.delete(db_classroom_time_slot)
            await session.commit()
        except NoResultFound:
            return None

        classroom_time_slot = ClassroomTimeSlotSchema.from_db_instance(db_classroom_time_slot)

        return classroom_time_slot
