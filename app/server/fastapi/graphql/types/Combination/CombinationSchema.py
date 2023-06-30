from typing import Optional, List

import strawberry
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError
from strawberry.types import Info

from app.server.database.database import async_session_maker
from app.server.database.models import Combination
from app.server.fastapi.graphql.types.User.UserSchema import UserSchema
from app.server.fastapi.graphql.types.Project.ProjectSchema import ProjectSchema


@strawberry.type
class CombinationSchema:
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
    def from_db_instance(db_instance: Combination) -> "CombinationSchema":
        return CombinationSchema(
            id=db_instance.id,
            name=db_instance.name,
            color=db_instance.color,
            user_id=db_instance.user,
            project_id=db_instance.project
        )


async def get_all_combinations(project_id: Optional[int] = None, user_id: Optional[int] = None) -> List[CombinationSchema]:
    async with async_session_maker() as session:
        statement = select(Combination).where(user_id is None or (Combination.project == project_id and Combination.user == user_id))
        db_combinations = (await session.execute(statement)).scalars().all()

        combinations = [CombinationSchema.from_db_instance(db_combination) for db_combination in db_combinations]

        return combinations


async def create_combination(name: str, color: Optional[str], user_id: int, project_id: int) -> Optional[CombinationSchema]:
    async with async_session_maker() as session:
        try:
            db_combination = Combination(
                name=name,
                color=color,
                user=user_id,
                project=project_id
            )
            session.add(db_combination)
            await session.commit()
        except IntegrityError:
            return None

        combination = CombinationSchema.from_db_instance(db_combination)

        return combination


async def update_combination(id: int, name: str, color: Optional[str], user_id: int, project_id: int) -> Optional[CombinationSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(Combination).where(Combination.id == id and Combination.user == user_id)
            db_combination = (await session.execute(statement)).scalars().one()
            db_combination.name = name
            db_combination.color = color
            db_combination.user = user_id
            db_combination.project = project_id
            await session.commit()
        except (NoResultFound, IntegrityError):
            return None

        combination = CombinationSchema.from_db_instance(db_combination)

        return combination


async def delete_combination(id: int, user_id: int) -> Optional[CombinationSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(Combination).where(Combination.id == id and Combination.user == user_id)
            db_combination = (await session.execute(statement)).scalars().one()
            await session.delete(db_combination)
            await session.commit()
        except NoResultFound:
            return None

        combination = CombinationSchema.from_db_instance(db_combination)

        return combination
