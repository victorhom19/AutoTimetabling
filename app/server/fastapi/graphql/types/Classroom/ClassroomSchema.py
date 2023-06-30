from typing import List, Optional



import strawberry
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError
from strawberry.types import Info

from app.server.database.database import async_session_maker
from app.server.database.models import Classroom, ClassroomEquipment, ClassroomTimeSlot
from app.server.fastapi.graphql.types.ClassroomEquipment.ClassroomEquipmentSchema import ClassroomEquipmentSchema
from app.server.fastapi.graphql.types.utils import group_by

from app.server.fastapi.graphql.types.User.UserSchema import UserSchema


@strawberry.type
class ClassroomSchema:
    id: int

    building: str
    auditory_number: str
    capacity: int

    user_id: int
    classroom_equipment_ids: List[int]
    classroom_time_slot_ids: List[int]

    @strawberry.field
    async def user(self, info: Info) -> UserSchema:
        return await info.context['user_loader'].load(self.user_id)
    
    @strawberry.field
    async def classroom_equipments(self, info: Info) -> List[ClassroomEquipmentSchema]:
        return await info.context['classroom_equipment_loader'].load_many(self.classroom_equipment_ids)

    @strawberry.field
    async def classroom_time_slots(self, info: Info) -> List[ClassroomEquipmentSchema]:
        return await info.context['classroom_equipment_loader'].load_many(self.classroom_equipment_ids)
    
    @staticmethod
    def from_db_instance(db_instance: Classroom, classroom_equipment_ids: List[int],
                         classroom_time_slot_ids: List[int]) -> "ClassroomSchema":
        return ClassroomSchema(
            id=db_instance.id,
            building=db_instance.building,
            auditory_number=db_instance.auditory_number,
            capacity=db_instance.capacity,
            user_id=db_instance.user,
            classroom_equipment_ids=classroom_equipment_ids,
            classroom_time_slot_ids=classroom_time_slot_ids
        )


async def get_all_classrooms(user_id: Optional[int] = None) -> List[ClassroomSchema]:


    equipment_ids_bucket = {}

    classrooms = []

    async with async_session_maker() as session:
        statement = select(Classroom, ClassroomEquipment) \
            .outerjoin(ClassroomEquipment, Classroom.id == ClassroomEquipment.classroom) \
            .where(user_id is None or Classroom.user == user_id)

        data = (await session.execute(statement)).all()

        for db_classroom, db_classroom_equipments in group_by(data):
            equipment_ids = []
            for [db_classroom_equipment] in db_classroom_equipments:
                if db_classroom_equipment:
                    equipment_ids.append(db_classroom_equipment.id)
            equipment_ids_bucket[db_classroom.id] = equipment_ids


        statement = select(Classroom, ClassroomTimeSlot) \
            .outerjoin(ClassroomTimeSlot, Classroom.id == ClassroomTimeSlot.classroom) \
            .where(user_id is None or Classroom.user == user_id)

        data = (await session.execute(statement)).all()

        for db_classroom, db_classroom_time_slots in group_by(data):
            time_slot_ids = []
            for [db_classroom_time_slot] in db_classroom_time_slots:
                if db_classroom_time_slot:
                    time_slot_ids.append(db_classroom_time_slot.id)

            classroom = ClassroomSchema.from_db_instance(
                db_classroom,
                classroom_equipment_ids=equipment_ids_bucket[db_classroom.id],
                classroom_time_slot_ids=time_slot_ids
            )

            classrooms.append(classroom)

        return classrooms


async def create_classroom(building: str, auditory_number: str, capacity: int, user_id: int) -> Optional[ClassroomSchema]:
    async with async_session_maker() as session:
        try:
            db_classroom = Classroom(
                building=building,
                auditory_number=auditory_number,
                capacity=capacity,
                user=user_id
            )
            session.add(db_classroom)
            await session.commit()
        except IntegrityError:
            return None

        classroom = ClassroomSchema.from_db_instance(db_classroom, [], [])

        return classroom


async def update_classroom(id: int, building: str, auditory_number: str, capacity: int, user_id: int) -> Optional[ClassroomSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(Classroom, ClassroomEquipment) \
                .outerjoin(ClassroomEquipment, Classroom.id == ClassroomEquipment.classroom) \
                .where(Classroom.id == id and Classroom.user == user_id)
            data = (await session.execute(statement)).all()

            [(db_classroom, db_classroom_equipments)] = group_by(data)
            equipment_ids = []
            for [db_classroom_equipment] in db_classroom_equipments:
                if db_classroom_equipment:
                    equipment_ids.append(db_classroom_equipment.id)

            statement = select(Classroom, ClassroomTimeSlot) \
                .outerjoin(ClassroomTimeSlot, Classroom.id == ClassroomTimeSlot.classroom) \
                .where(Classroom.id == id and Classroom.user == user_id)
            data = (await session.execute(statement)).all()

            [(db_classroom, db_classroom_time_slots)] = group_by(data)
            time_slot_ids = []
            for [db_classroom_time_slot] in db_classroom_time_slots:
                if db_classroom_time_slot:
                    time_slot_ids.append(db_classroom_time_slot.id)

            # Update database entity
            db_classroom.building = building
            db_classroom.auditory_number = auditory_number
            db_classroom.capacity = capacity
            db_classroom.user = user_id
            await session.commit()

        except NoResultFound:
            return None

        classroom = ClassroomSchema.from_db_instance(db_classroom, equipment_ids, time_slot_ids)

        return classroom


async def delete_classroom(id: int, user_id:int) -> Optional[ClassroomSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(Classroom).where(Classroom.id == id and Classroom.user == user_id)
            db_classroom = (await session.execute(statement)).one()

            await session.delete(db_classroom)
            await session.commit()

        except NoResultFound:
            return None
        
        classroom = ClassroomSchema.from_db_instance(db_classroom, [], [])

        return classroom
