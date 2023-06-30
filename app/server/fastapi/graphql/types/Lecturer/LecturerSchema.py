from typing import List, Optional



import strawberry
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError
from strawberry.types import Info

from app.server.database.database import async_session_maker
from app.server.database.models import Lecturer, Preference
from app.server.fastapi.graphql.types.Preference.PreferenceSchema import PreferenceSchema
from app.server.fastapi.graphql.types.utils import group_by

from app.server.fastapi.graphql.types.User.UserSchema import UserSchema
from app.server.fastapi.graphql.types.Department.DepartmentSchema import DepartmentSchema


@strawberry.type
class LecturerSchema:
    id: int

    name: str
    email: Optional[str]

    user_id: int
    department_id: int
    preference_ids: List[int]
    
    @strawberry.field
    async def user(self, info: Info) -> UserSchema:
        return await info.context['user_loader'].load(self.user_id)

    @strawberry.field
    async def department(self, info: Info) -> DepartmentSchema:
        return await info.context['department_loader'].load(self.department_id)
    
    @strawberry.field
    async def preferences(self, info: Info) -> List[PreferenceSchema]:
        return await info.context['preference_loader'].load_many(self.preference_ids)
    
    @staticmethod
    def from_db_instance(db_instance: Lecturer, preference_ids: List[int]) -> "LecturerSchema":
        return LecturerSchema(
            id=db_instance.id,
            name=db_instance.name,
            email=db_instance.email,
            user_id=db_instance.user,
            department_id=db_instance.department,
            preference_ids=preference_ids
        )

async def get_all_lecturers(user_id: Optional[int] = None) -> List[LecturerSchema]:
    async with async_session_maker() as session:
        statement = select(Lecturer, Preference) \
            .outerjoin(Preference, Lecturer.id == Preference.lecturer) \
            .where(user_id is None or Lecturer.user == user_id)

        data = (await session.execute(statement)).all()

        lecturers = []

        for db_lecturer, db_preferences in group_by(data):
            equipment_ids = []
            for [db_preference] in db_preferences:
                if db_preference:
                    equipment_ids.append(db_preference.id)

            lecturer = LecturerSchema.from_db_instance(db_lecturer, equipment_ids)
            lecturers.append(lecturer)

        return lecturers


async def create_lecturer(name: str, email: Optional[str], user_id: int, department_id: int) -> Optional[LecturerSchema]:
    async with async_session_maker() as session:
        try:
            db_lecturer = Lecturer(
                name=name,
                email=email,
                user=user_id,
                department=department_id
            )
            session.add(db_lecturer)
            await session.commit()
        except IntegrityError:
            return None

        lecturer = LecturerSchema.from_db_instance(db_lecturer, [])

        return lecturer


async def update_lecturer(id: int, name: str, email: Optional[str], user_id: int, department_id: int) -> Optional[LecturerSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(Lecturer, Preference) \
                .outerjoin(Preference, Lecturer.id == Preference.lecturer) \
                .where(Lecturer.id == id and Lecturer.user == user_id)
            data = (await session.execute(statement)).all()

            [(db_lecturer, db_preferences)] = group_by(data)
            equipment_ids = []
            for [db_preference] in db_preferences:
                if db_preference:
                    equipment_ids.append(db_preference.id)

            # Update database entity
            db_lecturer.name = name
            db_lecturer.email = email
            db_lecturer.user = user_id
            db_lecturer.department = department_id
            await session.commit()

        except NoResultFound:
            return None

        lecturer = LecturerSchema.from_db_instance(db_lecturer, equipment_ids)

        return lecturer


async def delete_lecturer(id: int, user_id:int) -> Optional[LecturerSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(Lecturer).where(Lecturer.id == id and Lecturer.user == user_id)
            db_lecturer = (await session.execute(statement)).one()

            await session.delete(db_lecturer)
            await session.commit()

        except NoResultFound:
            return None
        
        lecturer = LecturerSchema.from_db_instance(db_lecturer, [])

        return lecturer
