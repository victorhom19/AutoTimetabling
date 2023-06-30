from typing import Optional, List

import strawberry
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError
from strawberry.types import Info

from app.server.database.database import async_session_maker
from app.server.database.models import EducationProgram
from app.server.fastapi.graphql.types.User.UserSchema import UserSchema


@strawberry.type
class EducationProgramSchema:
    id: int
    
    name: str
    code: str
    profile_name: str
    profile_code: str
    education_level: str
    
    user_id: int
    
    @strawberry.field
    async def user(self, info: Info) -> UserSchema:
        return await info.context['user_loader'].load(self.user_id)

    @staticmethod
    def from_db_instance(db_instance: EducationProgram) -> "EducationProgramSchema":
        return EducationProgramSchema(
            id=db_instance.id,
            name=db_instance.name,
            code=db_instance.code,
            profile_name=db_instance.profile_name,
            profile_code=db_instance.profile_code,
            education_level=db_instance.education_level,
            user_id=db_instance.user
        )


async def get_all_education_programs(user_id: Optional[int] = None) -> List[EducationProgramSchema]:
    async with async_session_maker() as session:
        statement = select(EducationProgram).where(user_id is None or EducationProgram.user == user_id)
        db_education_programs = (await session.execute(statement)).scalars().all()

        education_programs = [EducationProgramSchema.from_db_instance(db_education_program) for db_education_program in db_education_programs]

        return education_programs


async def create_education_program(name: str, code: str, profile_name: str, profile_code: str, education_level: str, user_id: int) -> Optional[EducationProgramSchema]:
    async with async_session_maker() as session:
        try:
            if education_level == 'Бакалавриат':
                education_level = EducationProgram.EducationLevel.BACHELOR
            elif education_level == 'Магистратура':
                education_level = EducationProgram.EducationLevel.MASTER
            elif education_level == 'Специалитет':
                education_level = EducationProgram.EducationLevel.SPECIALIST
            elif education_level == 'Аспирантура':
                education_level = EducationProgram.EducationLevel.POSTGRADUATE


            db_education_program = EducationProgram(
                name=name,
                code=code,
                profile_name=profile_name,
                profile_code=profile_code,
                education_level=education_level,
                user=user_id
            )
            session.add(db_education_program)
            await session.commit()
        except IntegrityError:
            return None

        education_program = EducationProgramSchema.from_db_instance(db_education_program)

        return education_program


async def update_education_program(id: int, name: str, code: str, profile_name: str, profile_code: str, education_level: str, user_id: int) -> Optional[EducationProgramSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(EducationProgram).where(EducationProgram.id == id and EducationProgram.user == user_id)
            db_education_program = (await session.execute(statement)).scalars().one()
            db_education_program.name = name
            db_education_program.code = code
            db_education_program.profile_name = profile_name
            db_education_program.profile_code = profile_code
            db_education_program.education_level = education_level
            db_education_program.user = user_id
            await session.commit()
        except (NoResultFound, IntegrityError):
            return None

        education_program = EducationProgramSchema.from_db_instance(db_education_program)

        return education_program


async def delete_education_program(id: int, user_id: int) -> Optional[EducationProgramSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(EducationProgram).where(EducationProgram.id == id and EducationProgram.user == user_id)
            db_education_program = (await session.execute(statement)).scalars().one()
            await session.delete(db_education_program)
            await session.commit()
        except NoResultFound:
            return None

        education_program = EducationProgramSchema.from_db_instance(db_education_program)

        return education_program
