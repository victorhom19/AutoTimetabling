from typing import Optional, List

import strawberry
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError
from strawberry.types import Info

from app.server.database.database import async_session_maker
from app.server.database.models import Chain
from app.server.fastapi.graphql.types.User.UserSchema import UserSchema
from app.server.fastapi.graphql.types.Project.ProjectSchema import ProjectSchema


@strawberry.type
class ChainSchema:
    id: int
    
    name: str
    color: Optional[str]
    
    user_id: int
    project_id: int
    
    @strawberry.field
    async def user(self, info: Info) -> UserSchema:
        return await info.context['user_loader'].load(self.user_id)

    @strawberry.field
    async def project(self, info: Info) -> ProjectSchema:
        return await info.context['project_loader'].load(self.project_id)

    @staticmethod
    def from_db_instance(db_instance: Chain) -> "ChainSchema":
        return ChainSchema(
            id=db_instance.id,
            name=db_instance.name,
            color=db_instance.color,
            user_id=db_instance.user,
            project_id=db_instance.project
        )


async def get_all_chains(project_id: Optional[int] = None, user_id: Optional[int] = None) -> List[ChainSchema]:
    async with async_session_maker() as session:
        statement = select(Chain).where(user_id is None or (Chain.project == project_id and Chain.user == user_id))
        db_chains = (await session.execute(statement)).scalars().all()

        chains = [ChainSchema.from_db_instance(db_chain) for db_chain in db_chains]

        return chains


async def create_chain(name: str, color: Optional[str], user_id: int, project_id: int) -> Optional[ChainSchema]:
    async with async_session_maker() as session:
        try:
            db_chain = Chain(
                name=name,
                color=color,
                user=user_id,
                project=project_id
            )
            session.add(db_chain)
            await session.commit()
        except IntegrityError:
            return None

        chain = ChainSchema.from_db_instance(db_chain)

        return chain


async def update_chain(id: int, name: str, color: Optional[str], user_id: int, project_id: int) -> Optional[ChainSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(Chain).where(Chain.id == id and Chain.user == user_id)
            db_chain = (await session.execute(statement)).scalars().one()
            db_chain.name = name
            db_chain.color = color
            db_chain.user = user_id
            db_chain.project = project_id
            await session.commit()
        except (NoResultFound, IntegrityError):
            return None

        chain = ChainSchema.from_db_instance(db_chain)

        return chain


async def delete_chain(id: int, user_id: int) -> Optional[ChainSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(Chain).where(Chain.id == id and Chain.user == user_id)
            db_chain = (await session.execute(statement)).scalars().one()
            await session.delete(db_chain)
            await session.commit()
        except NoResultFound:
            return None

        chain = ChainSchema.from_db_instance(db_chain)

        return chain
