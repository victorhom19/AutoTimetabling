from typing import Optional, List

import strawberry
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError
from strawberry.types import Info

from app.server.database.database import async_session_maker
from app.server.database.models import Discipline
from app.server.fastapi.graphql.types.User.UserSchema import UserSchema
from app.server.fastapi.graphql.types.EducationModule.EducationModuleSchema import EducationModuleSchema


@strawberry.type
class DisciplineSchema:
    id: int
    
    name: str
    assessment: str
    
    user_id: int
    education_module_id: int
    
    @strawberry.field
    async def user(self, info: Info) -> UserSchema:
        return await info.context['user_loader'].load(self.user_id)

    @strawberry.field
    async def education_module(self, info: Info) -> EducationModuleSchema:
        return await info.context['education_module_loader'].load(self.education_module_id)

    @staticmethod
    def from_db_instance(db_instance: Discipline) -> "DisciplineSchema":
        return DisciplineSchema(
            id=db_instance.id,
            name=db_instance.name,
            assessment=db_instance.assessment,
            user_id=db_instance.user,
            education_module_id=db_instance.education_module
        )


async def get_all_disciplines(user_id: Optional[int] = None) -> List[DisciplineSchema]:
    async with async_session_maker() as session:
        statement = select(Discipline).where(user_id is None or Discipline.user == user_id)
        db_disciplines = (await session.execute(statement)).scalars().all()

        disciplines = [DisciplineSchema.from_db_instance(db_discipline) for db_discipline in db_disciplines]

        return disciplines


async def create_discipline(name: str, assessment: str, user_id: int, education_module_id: int) -> Optional[DisciplineSchema]:
    async with async_session_maker() as session:
        try:
            db_discipline = Discipline(
                name=name,
                assessment=assessment,
                user=user_id,
                education_module=education_module_id
            )
            session.add(db_discipline)
            await session.commit()
        except IntegrityError:
            return None

        discipline = DisciplineSchema.from_db_instance(db_discipline)

        return discipline


async def update_discipline(id: int, name: str, assessment: str, user_id: int, education_module_id: int) -> Optional[DisciplineSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(Discipline).where(Discipline.id == id and Discipline.user == user_id)
            db_discipline = (await session.execute(statement)).scalars().one()
            db_discipline.name = name
            db_discipline.assessment = assessment
            db_discipline.user = user_id
            db_discipline.education_module = education_module_id
            await session.commit()
        except (NoResultFound, IntegrityError):
            return None

        discipline = DisciplineSchema.from_db_instance(db_discipline)

        return discipline


async def delete_discipline(id: int, user_id: int) -> Optional[DisciplineSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(Discipline).where(Discipline.id == id and Discipline.user == user_id)
            db_discipline = (await session.execute(statement)).scalars().one()
            await session.delete(db_discipline)
            await session.commit()
        except NoResultFound:
            return None

        discipline = DisciplineSchema.from_db_instance(db_discipline)

        return discipline
