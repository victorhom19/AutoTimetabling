from typing import Optional, List

import strawberry
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError
from strawberry.types import Info

from app.server.database.database import async_session_maker
from app.server.database.models import EducationBlock
from app.server.fastapi.graphql.types.User.UserSchema import UserSchema
from app.server.fastapi.graphql.types.EducationProgram.EducationProgramSchema import EducationProgramSchema


@strawberry.type
class EducationBlockSchema:
    id: int
    
    name: str
    code: str
    
    user_id: int
    education_program_id: int
    
    @strawberry.field
    async def user(self, info: Info) -> UserSchema:
        return await info.context['user_loader'].load(self.user_id)

    @strawberry.field
    async def education_program(self, info: Info) -> EducationProgramSchema:
        return await info.context['education_program_loader'].load(self.education_program_id)

    @staticmethod
    def from_db_instance(db_instance: EducationBlock) -> "EducationBlockSchema":
        return EducationBlockSchema(
            id=db_instance.id,
            name=db_instance.name,
            code=db_instance.code,
            user_id=db_instance.user,
            education_program_id=db_instance.education_program
        )


async def get_all_education_blocks(user_id: Optional[int] = None) -> List[EducationBlockSchema]:
    async with async_session_maker() as session:
        statement = select(EducationBlock).where(user_id is None or EducationBlock.user == user_id)
        db_education_blocks = (await session.execute(statement)).scalars().all()

        education_blocks = [EducationBlockSchema.from_db_instance(db_education_block) for db_education_block in db_education_blocks]

        return education_blocks


async def create_education_block(name: str, code: str, user_id: int, education_program_id: int) -> Optional[EducationBlockSchema]:
    async with async_session_maker() as session:
        try:
            db_education_block = EducationBlock(
                name=name,
                code=code,
                user=user_id,
                education_program=education_program_id
            )
            session.add(db_education_block)
            await session.commit()
        except IntegrityError:
            return None

        education_block = EducationBlockSchema.from_db_instance(db_education_block)

        return education_block


async def update_education_block(id: int, name: str, code: str, user_id: int, education_program_id: int) -> Optional[EducationBlockSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(EducationBlock).where(EducationBlock.id == id and EducationBlock.user == user_id)
            db_education_block = (await session.execute(statement)).scalars().one()
            db_education_block.name = name
            db_education_block.code = code
            db_education_block.user = user_id
            db_education_block.education_program = education_program_id
            await session.commit()
        except (NoResultFound, IntegrityError):
            return None

        education_block = EducationBlockSchema.from_db_instance(db_education_block)

        return education_block


async def delete_education_block(id: int, user_id: int) -> Optional[EducationBlockSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(EducationBlock).where(EducationBlock.id == id and EducationBlock.user == user_id)
            db_education_block = (await session.execute(statement)).scalars().one()
            await session.delete(db_education_block)
            await session.commit()
        except NoResultFound:
            return None

        education_block = EducationBlockSchema.from_db_instance(db_education_block)

        return education_block
