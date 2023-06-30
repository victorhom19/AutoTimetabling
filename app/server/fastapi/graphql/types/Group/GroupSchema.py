from typing import Optional, List

import strawberry
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError
from strawberry.types import Info

from app.server.database.database import async_session_maker
from app.server.database.models import Group
from app.server.fastapi.graphql.types.User.UserSchema import UserSchema
from app.server.fastapi.graphql.types.EducationProgram.EducationProgramSchema import EducationProgramSchema
from app.server.fastapi.graphql.types.Department.DepartmentSchema import DepartmentSchema


@strawberry.type
class GroupSchema:
    id: int
    
    code: str
    size: int
    
    user_id: int
    group_id: int
    education_program_id: int
    department_id: int
    
    @strawberry.field
    async def user(self, info: Info) -> UserSchema:
        return await info.context['user_loader'].load(self.user_id)

    @strawberry.field
    async def part_of(self, info: Info) -> 'GroupSchema':
        return await info.context['group_loader'].load(self.group_id)

    @strawberry.field
    async def education_program(self, info: Info) -> EducationProgramSchema:
        return await info.context['education_program_loader'].load(self.education_program_id)

    @strawberry.field
    async def department(self, info: Info) -> DepartmentSchema:
        return await info.context['department_loader'].load(self.department_id)

    @staticmethod
    def from_db_instance(db_instance: Group) -> "GroupSchema":
        return GroupSchema(
            id=db_instance.id,
            code=db_instance.code,
            size=db_instance.size,
            user_id=db_instance.user,
            group_id=db_instance.part_of,
            education_program_id=db_instance.education_program,
            department_id=db_instance.department
        )


async def get_all_groups(user_id: Optional[int] = None) -> List[GroupSchema]:
    async with async_session_maker() as session:
        statement = select(Group).where(user_id is None or Group.user == user_id)
        db_groups = (await session.execute(statement)).scalars().all()

        groups = [GroupSchema.from_db_instance(db_group) for db_group in db_groups]

        return groups


async def create_group(code: str, size: int, user_id: int, group_id: int, education_program_id: int, department_id: int) -> Optional[GroupSchema]:
    async with async_session_maker() as session:
        try:
            db_group = Group(
                code=code,
                size=size,
                user=user_id,
                part_of=group_id,
                education_program=education_program_id,
                department=department_id
            )
            session.add(db_group)
            await session.commit()
        except IntegrityError:
            return None

        group = GroupSchema.from_db_instance(db_group)

        return group


async def update_group(id: int, code: str, size: int, user_id: int, group_id: int, education_program_id: int, department_id: int) -> Optional[GroupSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(Group).where(Group.id == id and Group.user == user_id)
            db_group = (await session.execute(statement)).scalars().one()
            db_group.code = code
            db_group.size = size
            db_group.user = user_id
            db_group.part_of = group_id
            db_group.education_program = education_program_id
            db_group.department = department_id
            await session.commit()
        except (NoResultFound, IntegrityError):
            return None

        group = GroupSchema.from_db_instance(db_group)

        return group


async def delete_group(id: int, user_id: int) -> Optional[GroupSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(Group).where(Group.id == id and Group.user == user_id)
            db_group = (await session.execute(statement)).scalars().one()
            await session.delete(db_group)
            await session.commit()
        except NoResultFound:
            return None

        group = GroupSchema.from_db_instance(db_group)

        return group
