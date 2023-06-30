from typing import Optional, List

import strawberry
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError
from strawberry.types import Info

from app.server.database.database import async_session_maker
from app.server.database.models import Preference
from app.server.fastapi.graphql.types.User.UserSchema import UserSchema
from app.server.fastapi.graphql.types.Project.ProjectSchema import ProjectSchema
from app.server.fastapi.graphql.types.TimeSlot.TimeSlotSchema import TimeSlotSchema


@strawberry.type
class PreferenceSchema:
    id: int
    
    value: int
    
    user_id: int
    project_id: int
    lecturer_id: int
    time_slot_id: int
    
    @strawberry.field
    async def user(self, info: Info) -> UserSchema:
        return await info.context['user_loader'].load(self.user_id)

    @strawberry.field
    async def project(self, info: Info) -> ProjectSchema:
        return await info.context['project_loader'].load(self.project_id)

    @strawberry.field
    async def time_slot(self, info: Info) -> TimeSlotSchema:
        return await info.context['time_slot_loader'].load(self.time_slot_id)

    @staticmethod
    def from_db_instance(db_instance: Preference) -> "PreferenceSchema":
        return PreferenceSchema(
            id=db_instance.id,
            value=db_instance.value,
            user_id=db_instance.user,
            project_id=db_instance.project,
            lecturer_id=db_instance.lecturer,
            time_slot_id=db_instance.time_slot
        )


async def get_all_preferences(project_id: Optional[int] = None, user_id: Optional[int] = None) -> List[PreferenceSchema]:
    async with async_session_maker() as session:
        statement = select(Preference).where(user_id is None or (Preference.project == project_id and Preference.user == user_id))
        db_preferences = (await session.execute(statement)).scalars().all()

        preferences = [PreferenceSchema.from_db_instance(db_preference) for db_preference in db_preferences]

        return preferences


async def create_preference(value: int, user_id: int, project_id: int, lecturer_id: int, time_slot_id: int) -> Optional[PreferenceSchema]:
    async with async_session_maker() as session:
        try:
            db_preference = Preference(
                value=value,
                user=user_id,
                project=project_id,
                lecturer=lecturer_id,
                time_slot=time_slot_id
            )
            session.add(db_preference)
            await session.commit()
        except IntegrityError:
            return None

        preference = PreferenceSchema.from_db_instance(db_preference)

        return preference


async def update_preference(id: int, value: int, user_id: int, project_id: int, lecturer_id: int, time_slot_id: int) -> Optional[PreferenceSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(Preference).where(Preference.id == id and Preference.user == user_id)
            db_preference = (await session.execute(statement)).scalars().one()
            db_preference.value = value
            db_preference.user = user_id
            db_preference.project = project_id
            db_preference.lecturer = lecturer_id
            db_preference.time_slot = time_slot_id
            await session.commit()
        except (NoResultFound, IntegrityError):
            return None

        preference = PreferenceSchema.from_db_instance(db_preference)

        return preference


async def delete_preference(id: int, user_id: int) -> Optional[PreferenceSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(Preference).where(Preference.id == id and Preference.user == user_id)
            db_preference = (await session.execute(statement)).scalars().one()
            await session.delete(db_preference)
            await session.commit()
        except NoResultFound:
            return None

        preference = PreferenceSchema.from_db_instance(db_preference)

        return preference
