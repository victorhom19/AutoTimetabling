from typing import List, Optional



import strawberry
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError
from strawberry.types import Info

from app.server.database.database import async_session_maker
from app.server.database.models import ClassroomPool, ClassroomPoolClassroom
from app.server.fastapi.graphql.types.ClassroomPoolClassroom.ClassroomPoolClassroomSchema import ClassroomPoolClassroomSchema
from app.server.fastapi.graphql.types.utils import group_by

from app.server.fastapi.graphql.types.User.UserSchema import UserSchema


@strawberry.type
class ClassroomPoolSchema:
    id: int

    name: str
    color: Optional[str]

    user_id: int
    classroom_pool_classroom_ids: List[int]
    
    @strawberry.field
    async def user(self, info: Info) -> UserSchema:
        return await info.context['user_loader'].load(self.user_id)
    
    @strawberry.field
    async def classroom_pool_classrooms(self, info: Info) -> List[ClassroomPoolClassroomSchema]:
        return await info.context['classroom_pool_classroom_loader'].load_many(self.classroom_pool_classroom_ids)
    
    @staticmethod
    def from_db_instance(db_instance: ClassroomPool, classroom_pool_classroom_ids: List[int]) -> "ClassroomPoolSchema":
        return ClassroomPoolSchema(
            id=db_instance.id,
            name=db_instance.name,
            color=db_instance.color,
            user_id=db_instance.user,
            classroom_pool_classroom_ids=classroom_pool_classroom_ids
        )

async def get_all_classroom_pools(user_id: Optional[int] = None) -> List[ClassroomPoolSchema]:
    async with async_session_maker() as session:
        statement = select(ClassroomPool, ClassroomPoolClassroom) \
            .outerjoin(ClassroomPoolClassroom, ClassroomPool.id == ClassroomPoolClassroom.classroom_pool) \
            .where(user_id is None or ClassroomPool.user == user_id)

        data = (await session.execute(statement)).all()

        classroom_pools = []

        for db_classroom_pool, db_classroom_pool_classrooms in group_by(data):
            equipment_ids = []
            for [db_classroom_pool_classroom] in db_classroom_pool_classrooms:
                if db_classroom_pool_classroom:
                    equipment_ids.append(db_classroom_pool_classroom.id)

            classroom_pool = ClassroomPoolSchema.from_db_instance(db_classroom_pool, equipment_ids)
            classroom_pools.append(classroom_pool)

        return classroom_pools


async def create_classroom_pool(name: str, color: Optional[str], user_id: int) -> Optional[ClassroomPoolSchema]:
    async with async_session_maker() as session:
        try:
            db_classroom_pool = ClassroomPool(
                name=name,
                color=color,
                user=user_id
            )
            session.add(db_classroom_pool)
            await session.commit()
        except IntegrityError:
            return None

        classroom_pool = ClassroomPoolSchema.from_db_instance(db_classroom_pool, [])

        return classroom_pool


async def update_classroom_pool(id: int, name: str, color: Optional[str], user_id: int) -> Optional[ClassroomPoolSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(ClassroomPool, ClassroomPoolClassroom) \
                .outerjoin(ClassroomPoolClassroom, ClassroomPool.id == ClassroomPoolClassroom.classroom_pool) \
                .where(ClassroomPool.id == id and ClassroomPool.user == user_id)
            data = (await session.execute(statement)).all()

            [(db_classroom_pool, db_classroom_pool_classrooms)] = group_by(data)
            equipment_ids = []
            for [db_classroom_pool_classroom] in db_classroom_pool_classrooms:
                if db_classroom_pool_classroom:
                    equipment_ids.append(db_classroom_pool_classroom.id)

            # Update database entity
            db_classroom_pool.name = name
            db_classroom_pool.color = color
            db_classroom_pool.user = user_id
            await session.commit()

        except NoResultFound:
            return None

        classroom_pool = ClassroomPoolSchema.from_db_instance(db_classroom_pool, equipment_ids)

        return classroom_pool


async def delete_classroom_pool(id: int, user_id:int) -> Optional[ClassroomPoolSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(ClassroomPool).where(ClassroomPool.id == id and ClassroomPool.user == user_id)
            db_classroom_pool = (await session.execute(statement)).one()

            await session.delete(db_classroom_pool)
            await session.commit()

        except NoResultFound:
            return None
        
        classroom_pool = ClassroomPoolSchema.from_db_instance(db_classroom_pool, [])

        return classroom_pool
