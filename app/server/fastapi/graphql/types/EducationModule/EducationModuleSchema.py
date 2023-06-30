from typing import Optional, List

import strawberry
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError
from strawberry.types import Info

from app.server.database.database import async_session_maker
from app.server.database.models import EducationModule
from app.server.fastapi.graphql.types.User.UserSchema import UserSchema
from app.server.fastapi.graphql.types.EducationBlock.EducationBlockSchema import EducationBlockSchema


@strawberry.type
class EducationModuleSchema:
    id: int
    
    name: str
    code: str
    is_base_module: bool
    
    user_id: int
    education_module_id: int
    education_block_id: int
    
    @strawberry.field
    async def user(self, info: Info) -> UserSchema:
        return await info.context['user_loader'].load(self.user_id)

    @strawberry.field
    async def education_module(self, info: Info) -> "EducationModuleSchema":
        return await info.context['education_module_loader'].load(self.education_module_id)

    @strawberry.field
    async def education_block(self, info: Info) -> EducationBlockSchema:
        return await info.context['education_block_loader'].load(self.education_block_id)

    @staticmethod
    def from_db_instance(db_instance: EducationModule) -> "EducationModuleSchema":
        return EducationModuleSchema(
            id=db_instance.id,
            name=db_instance.name,
            code=db_instance.code,
            is_base_module=db_instance.is_base_module,
            user_id=db_instance.user,
            education_module_id=db_instance.education_module,
            education_block_id=db_instance.education_block
        )


async def get_all_education_modules(user_id: Optional[int] = None) -> List[EducationModuleSchema]:
    async with async_session_maker() as session:
        statement = select(EducationModule).where(user_id is None or EducationModule.user == user_id)
        db_education_modules = (await session.execute(statement)).scalars().all()

        education_modules = [EducationModuleSchema.from_db_instance(db_education_module) for db_education_module in db_education_modules]

        return education_modules


async def create_education_module(name: str, code: str, is_base_module: bool, user_id: int, education_module_id: int, education_block_id: int) -> Optional[EducationModuleSchema]:
    async with async_session_maker() as session:
        try:
            db_education_module = EducationModule(
                name=name,
                code=code,
                is_base_module=is_base_module,
                user=user_id,
                education_module=education_module_id,
                education_block=education_block_id
            )
            session.add(db_education_module)
            await session.commit()
        except IntegrityError:
            return None

        education_module = EducationModuleSchema.from_db_instance(db_education_module)

        return education_module


async def update_education_module(id: int, name: str, code: str, is_base_module: bool, user_id: int, education_module_id: int, education_block_id: int) -> Optional[EducationModuleSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(EducationModule).where(EducationModule.id == id and EducationModule.user == user_id)
            db_education_module = (await session.execute(statement)).scalars().one()
            db_education_module.name = name
            db_education_module.code = code
            db_education_module.is_base_module = is_base_module
            db_education_module.user = user_id
            db_education_module.education_module = education_module_id
            db_education_module.education_block = education_block_id
            await session.commit()
        except (NoResultFound, IntegrityError):
            return None

        education_module = EducationModuleSchema.from_db_instance(db_education_module)

        return education_module


async def delete_education_module(id: int, user_id: int) -> Optional[EducationModuleSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(EducationModule).where(EducationModule.id == id and EducationModule.user == user_id)
            db_education_module = (await session.execute(statement)).scalars().one()
            await session.delete(db_education_module)
            await session.commit()
        except NoResultFound:
            return None

        education_module = EducationModuleSchema.from_db_instance(db_education_module)

        return education_module
