from typing import Optional, List

import strawberry
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError
from strawberry.types import Info

from app.server.database.database import async_session_maker
from app.server.database.models import Course
from app.server.fastapi.graphql.types.User.UserSchema import UserSchema
from app.server.fastapi.graphql.types.Project.ProjectSchema import ProjectSchema
from app.server.fastapi.graphql.types.Discipline.DisciplineSchema import DisciplineSchema
from app.server.fastapi.graphql.types.Lecturer.LecturerSchema import LecturerSchema
from app.server.fastapi.graphql.types.Group.GroupSchema import GroupSchema
from app.server.fastapi.graphql.types.Combination.CombinationSchema import CombinationSchema
from app.server.fastapi.graphql.types.Chain.ChainSchema import ChainSchema
from app.server.fastapi.graphql.types.TimeSlot.TimeSlotSchema import TimeSlotSchema
from app.server.fastapi.graphql.types.ClassroomPool.ClassroomPoolSchema import ClassroomPoolSchema


@strawberry.type
class CourseSchema:
    id: int
    
    course_type: str
    duration: int
    week_intensity: int
    block_length: int
    chain_priority: Optional[int]
    
    user_id: int
    project_id: int
    discipline_id: int
    lecturer_id: int
    group_id: int
    combination_id: int
    chain_id: int
    time_slot_from_id: int
    time_slot_to_id: int
    classroom_pool_id: int
    
    @strawberry.field
    async def user(self, info: Info) -> UserSchema:
        return await info.context['user_loader'].load(self.user_id)

    @strawberry.field
    async def project(self, info: Info) -> ProjectSchema:
        return await info.context['project_loader'].load(self.project_id)

    @strawberry.field
    async def discipline(self, info: Info) -> DisciplineSchema:
        return await info.context['discipline_loader'].load(self.discipline_id)

    @strawberry.field
    async def lecturer(self, info: Info) -> LecturerSchema:
        return await info.context['lecturer_loader'].load(self.lecturer_id)

    @strawberry.field
    async def group(self, info: Info) -> GroupSchema:
        return await info.context['group_loader'].load(self.group_id)

    @strawberry.field
    async def combination(self, info: Info) -> CombinationSchema:
        return await info.context['combination_loader'].load(self.combination_id)

    @strawberry.field
    async def chain(self, info: Info) -> ChainSchema:
        return await info.context['chain_loader'].load(self.chain_id)

    @strawberry.field
    async def time_slot_from(self, info: Info) -> TimeSlotSchema:
        return await info.context['time_slot_loader'].load(self.time_slot_from_id)

    @strawberry.field
    async def time_slot_to(self, info: Info) -> TimeSlotSchema:
        return await info.context['time_slot_loader'].load(self.time_slot_to_id)

    @strawberry.field
    async def classroom_pool(self, info: Info) -> ClassroomPoolSchema:
        return await info.context['classroom_pool_loader'].load(self.classroom_pool_id)

    @staticmethod
    def from_db_instance(db_instance: Course) -> "CourseSchema":
        return CourseSchema(
            id=db_instance.id,
            course_type=db_instance.course_type,
            duration=db_instance.duration,
            week_intensity=db_instance.week_intensity,
            block_length=db_instance.block_length,
            chain_priority=db_instance.chain_priority,
            user_id=db_instance.user,
            project_id=db_instance.project,
            discipline_id=db_instance.discipline,
            lecturer_id=db_instance.lecturer,
            group_id=db_instance.group,
            combination_id=db_instance.combination,
            chain_id=db_instance.chain,
            time_slot_id=db_instance.time_slot,
            classroom_pool_id=db_instance.classroom_pool
        )


async def get_all_courses(project_id: Optional[int] = None, user_id: Optional[int] = None) -> List[CourseSchema]:
    async with async_session_maker() as session:
        statement = select(Course).where(user_id is None or (Course.project == project_id and Course.user == user_id))
        db_courses = (await session.execute(statement)).scalars().all()

        courses = [CourseSchema.from_db_instance(db_course) for db_course in db_courses]

        return courses


async def create_course(course_type: str, duration: int, week_intensity: int, block_length: int, chain_priority: Optional[int], user_id: int, project_id: int, discipline_id: int, lecturer_id: int, group_id: int, combination_id: int, chain_id: int, time_slot_id: int, classroom_pool_id: int) -> Optional[CourseSchema]:
    async with async_session_maker() as session:
        try:
            db_course = Course(
                course_type=course_type,
                duration=duration,
                week_intensity=week_intensity,
                block_length=block_length,
                chain_priority=chain_priority,
                user=user_id,
                project=project_id,
                discipline=discipline_id,
                lecturer=lecturer_id,
                group=group_id,
                combination=combination_id,
                chain=chain_id,
                time_slot_from=time_slot_id,
                time_slot_to=time_slot_id,
                classroom_pool=classroom_pool_id
            )
            session.add(db_course)
            await session.commit()
        except IntegrityError:
            return None

        course = CourseSchema.from_db_instance(db_course)

        return course


async def update_course(id: int, course_type: str, duration: int, week_intensity: int, block_length: int, chain_priority: Optional[int], user_id: int, project_id: int, discipline_id: int, lecturer_id: int, group_id: int, combination_id: int, chain_id: int, time_slot_id: int, classroom_pool_id: int) -> Optional[CourseSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(Course).where(Course.id == id and Course.user == user_id)
            db_course = (await session.execute(statement)).scalars().one()
            db_course.course_type = course_type
            db_course.duration = duration
            db_course.week_intensity = week_intensity
            db_course.block_length = block_length
            db_course.chain_priority = chain_priority
            db_course.user = user_id
            db_course.project = project_id
            db_course.discipline = discipline_id
            db_course.lecturer = lecturer_id
            db_course.group = group_id
            db_course.combination = combination_id
            db_course.chain = chain_id
            db_course.time_slot = time_slot_id
            db_course.classroom_pool = classroom_pool_id
            await session.commit()
        except (NoResultFound, IntegrityError):
            return None

        course = CourseSchema.from_db_instance(db_course)

        return course


async def delete_course(id: int, user_id: int) -> Optional[CourseSchema]:
    async with async_session_maker() as session:
        try:
            statement = select(Course).where(Course.id == id and Course.user == user_id)
            db_course = (await session.execute(statement)).scalars().one()
            await session.delete(db_course)
            await session.commit()
        except NoResultFound:
            return None

        course = CourseSchema.from_db_instance(db_course)

        return course
