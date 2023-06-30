from typing import Optional, List

import strawberry
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError
from strawberry.types import Info

from app.server.database.database import async_session_maker
from app.server.database.models import Institution
from app.server.fastapi.graphql.types.User.UserSchema import UserSchema


@strawberry.type
class InstitutionSchema:
    id: int
    
    code: str
    name: str
    
    user_id: int
    
    @strawberry.field
    async def user(self, info: Info) -> UserSchema:
        return await info.context['user_loader'].load(self.user_id)

    @staticmethod
    def from_db_instance(db_instance: Institution) -> "InstitutionSchema":
        return InstitutionSchema(
            id=db_instance.id,
            code=db_instance.code,
            name=db_instance.name,
            user_id=db_instance.user
        )


async def get_all_institutions(user_id: Optional[int] = None) -> List[InstitutionSchema]:
    async with async_session_maker() as session:
        statement = select(Institution).where(user_id is None or Institution.user == user_id)
        db_institutions = (await session.execute(statement)).scalars().all()

        institutions = [InstitutionSchema.from_db_instance(db_institution) for db_institution in db_institutions]

        return institutions


async def create_institution(code: str, name: str, user_id: int) -> Optional[InstitutionSchema]:
    async with async_session_maker() as session:
        try:
            db_institution = Institution(
                code=code,
                name=name,
                user=user_id
            )
            session.add(db_institution)
            await session.commit()
        except IntegrityError:
            return None

        institution = InstitutionSchema.from_db_instance(db_institution)

        return institution


async def update_institution(id: int, code: str, name: str, user_id: int) -> Optional[InstitutionSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(Institution).where(Institution.id == id and Institution.user == user_id)
            db_institution = (await session.execute(statement)).scalars().one()
            db_institution.code = code
            db_institution.name = name
            db_institution.user = user_id
            await session.commit()
        except (NoResultFound, IntegrityError):
            return None

        institution = InstitutionSchema.from_db_instance(db_institution)

        return institution


async def delete_institution(id: int, user_id: int) -> Optional[InstitutionSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(Institution).where(Institution.id == id and Institution.user == user_id)
            db_institution = (await session.execute(statement)).scalars().one()
            await session.delete(db_institution)
            await session.commit()
        except NoResultFound:
            return None

        institution = InstitutionSchema.from_db_instance(db_institution)

        return institution
