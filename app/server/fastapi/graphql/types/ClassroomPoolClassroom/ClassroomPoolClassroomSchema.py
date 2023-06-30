from typing import Optional, List

import strawberry
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError
from strawberry.types import Info

from app.server.database.database import async_session_maker
from app.server.database.models import ClassroomPoolClassroom
from app.server.fastapi.graphql.types.User.UserSchema import UserSchema
from app.server.fastapi.graphql.types.Classroom.ClassroomSchema import ClassroomSchema


@strawberry.type
class ClassroomPoolClassroomSchema:
    id: int
    
    
    
    user_id: int
    classroom_pool_id: int
    classroom_id: int
    
    @strawberry.field
    async def user(self, info: Info) -> UserSchema:
        return await info.context['user_loader'].load(self.user_id)

    @strawberry.field
    async def classroom(self, info: Info) -> ClassroomSchema:
        return await info.context['classroom_loader'].load(self.classroom_id)

    @staticmethod
    def from_db_instance(db_instance: ClassroomPoolClassroom) -> "ClassroomPoolClassroomSchema":
        return ClassroomPoolClassroomSchema(
            id=db_instance.id,
            user_id=db_instance.user,
            classroom_pool_id=db_instance.classroom_pool,
            classroom_id=db_instance.classroom
        )


async def get_all_classroom_pool_classrooms(user_id: Optional[int] = None) -> List[ClassroomPoolClassroomSchema]:
    async with async_session_maker() as session:
        statement = select(ClassroomPoolClassroom).where(user_id is None or ClassroomPoolClassroom.user == user_id)
        db_classroom_pool_classrooms = (await session.execute(statement)).scalars().all()

        classroom_pool_classrooms = [ClassroomPoolClassroomSchema.from_db_instance(db_classroom_pool_classroom) for db_classroom_pool_classroom in db_classroom_pool_classrooms]

        return classroom_pool_classrooms


async def create_classroom_pool_classroom(user_id: int, classroom_pool_id: int, classroom_id: int) -> Optional[ClassroomPoolClassroomSchema]:
    async with async_session_maker() as session:
        try:
            db_classroom_pool_classroom = ClassroomPoolClassroom(
                user=user_id,
                classroom_pool=classroom_pool_id,
                classroom=classroom_id
            )
            session.add(db_classroom_pool_classroom)
            await session.commit()
        except IntegrityError:
            return None

        classroom_pool_classroom = ClassroomPoolClassroomSchema.from_db_instance(db_classroom_pool_classroom)

        return classroom_pool_classroom


async def update_classroom_pool_classroom(id: int, user_id: int, classroom_pool_id: int, classroom_id: int) -> Optional[ClassroomPoolClassroomSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(ClassroomPoolClassroom).where(ClassroomPoolClassroom.id == id and ClassroomPoolClassroom.user == user_id)
            db_classroom_pool_classroom = (await session.execute(statement)).scalars().one()
            db_classroom_pool_classroom.user = user_id
            db_classroom_pool_classroom.classroom_pool = classroom_pool_id
            db_classroom_pool_classroom.classroom = classroom_id
            await session.commit()
        except (NoResultFound, IntegrityError):
            return None

        classroom_pool_classroom = ClassroomPoolClassroomSchema.from_db_instance(db_classroom_pool_classroom)

        return classroom_pool_classroom


async def delete_classroom_pool_classroom(id: int, user_id: int) -> Optional[ClassroomPoolClassroomSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(ClassroomPoolClassroom).where(ClassroomPoolClassroom.id == id and ClassroomPoolClassroom.user == user_id)
            db_classroom_pool_classroom = (await session.execute(statement)).scalars().one()
            await session.delete(db_classroom_pool_classroom)
            await session.commit()
        except NoResultFound:
            return None

        classroom_pool_classroom = ClassroomPoolClassroomSchema.from_db_instance(db_classroom_pool_classroom)

        return classroom_pool_classroom
