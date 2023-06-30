from typing import Optional, List

import strawberry
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError
from strawberry.types import Info

from app.server.database.database import async_session_maker
from app.server.database.models import Department
from app.server.fastapi.graphql.types.User.UserSchema import UserSchema
from app.server.fastapi.graphql.types.Institution.InstitutionSchema import InstitutionSchema


@strawberry.type
class DepartmentSchema:
    id: int
    
    name: str
    
    user_id: int
    institution_id: int
    
    @strawberry.field
    async def user(self, info: Info) -> UserSchema:
        return await info.context['user_loader'].load(self.user_id)

    @strawberry.field
    async def institution(self, info: Info) -> InstitutionSchema:
        return await info.context['institution_loader'].load(self.institution_id)

    @staticmethod
    def from_db_instance(db_instance: Department) -> "DepartmentSchema":
        return DepartmentSchema(
            id=db_instance.id,
            name=db_instance.name,
            user_id=db_instance.user,
            institution_id=db_instance.institution
        )


async def get_all_departments(user_id: Optional[int] = None) -> List[DepartmentSchema]:
    async with async_session_maker() as session:
        statement = select(Department).where(user_id is None or Department.user == user_id)
        db_departments = (await session.execute(statement)).scalars().all()

        departments = [DepartmentSchema.from_db_instance(db_department) for db_department in db_departments]

        return departments


async def create_department(name: str, user_id: int, institution_id: int) -> Optional[DepartmentSchema]:
    async with async_session_maker() as session:
        try:
            db_department = Department(
                name=name,
                user=user_id,
                institution=institution_id
            )
            session.add(db_department)
            await session.commit()
        except IntegrityError:
            return None

        department = DepartmentSchema.from_db_instance(db_department)

        return department


async def update_department(id: int, name: str, user_id: int, institution_id: int) -> Optional[DepartmentSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(Department).where(Department.id == id and Department.user == user_id)
            db_department = (await session.execute(statement)).scalars().one()
            db_department.name = name
            db_department.user = user_id
            db_department.institution = institution_id
            await session.commit()
        except (NoResultFound, IntegrityError):
            return None

        department = DepartmentSchema.from_db_instance(db_department)

        return department


async def delete_department(id: int, user_id: int) -> Optional[DepartmentSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(Department).where(Department.id == id and Department.user == user_id)
            db_department = (await session.execute(statement)).scalars().one()
            await session.delete(db_department)
            await session.commit()
        except NoResultFound:
            return None

        department = DepartmentSchema.from_db_instance(db_department)

        return department
