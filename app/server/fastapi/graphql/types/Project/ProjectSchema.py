from typing import Optional, List

import strawberry
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError
from strawberry.types import Info

from app.server.database.database import async_session_maker
from app.server.database.models import Project
from app.server.fastapi.graphql.types.User.UserSchema import UserSchema


@strawberry.type
class ProjectSchema:
    id: int
    
    name: str
    description: Optional[str]
    
    user_id: int
    
    @strawberry.field
    async def user(self, info: Info) -> UserSchema:
        return await info.context['user_loader'].load(self.user_id)

    @staticmethod
    def from_db_instance(db_instance: Project) -> "ProjectSchema":
        return ProjectSchema(
            id=db_instance.id,
            name=db_instance.name,
            description=db_instance.description,
            user_id=db_instance.user
        )


async def get_all_projects(user_id: Optional[int] = None) -> List[ProjectSchema]:
    async with async_session_maker() as session:
        statement = select(Project).where(user_id is None or Project.user == user_id)
        db_projects = (await session.execute(statement)).scalars().all()

        projects = [ProjectSchema.from_db_instance(db_project) for db_project in db_projects]

        return projects


async def create_project(name: str, description: Optional[str], user_id: int) -> Optional[ProjectSchema]:
    async with async_session_maker() as session:
        try:
            db_project = Project(
                name=name,
                description=description,
                user=user_id
            )
            session.add(db_project)
            await session.commit()
        except IntegrityError:
            return None

        project = ProjectSchema.from_db_instance(db_project)

        return project


async def update_project(id: int, name: str, description: Optional[str], user_id: int) -> Optional[ProjectSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(Project).where(Project.id == id and Project.user == user_id)
            db_project = (await session.execute(statement)).scalars().one()
            db_project.name = name
            db_project.description = description
            db_project.user = user_id
            await session.commit()
        except (NoResultFound, IntegrityError):
            return None

        project = ProjectSchema.from_db_instance(db_project)

        return project


async def delete_project(id: int, user_id: int) -> Optional[ProjectSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(Project).where(Project.id == id and Project.user == user_id)
            db_project = (await session.execute(statement)).scalars().one()
            await session.delete(db_project)
            await session.commit()
        except NoResultFound:
            return None

        project = ProjectSchema.from_db_instance(db_project)

        return project
