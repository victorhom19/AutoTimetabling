import asyncio
from typing import List, Type, Optional

from sqlalchemy import select

from app.server.database.database import async_session_maker
from app.server.database.models import Classroom as DatabaseClassroom, TimeSlot as DatabaseTimeslot, \
    Course as DatabaseCourse, ClassroomEquipment as DatabaseClassroomEquipment, \
    RequiredEquipment as DatabaseRequiredEquipment, ClassroomPool, ChainCourse, TimeInterval, Chain, CombinationCourse, \
    Combination, Group, Discipline, Lecturer, CourseType
from app.server.timetabling.base_solver import InitialBaseSolver, OptimizationBaseSolver
from app.server.timetabling.initial.solver.smt.z3.simplified_solver import Z3SimpleSolver
from app.server.timetabling.models.classroom import Classroom as ModelClassroom
from app.server.timetabling.models.classroom_equipment import ClassroomEquipment
from app.server.timetabling.models.course import Course
from app.server.timetabling.models.required_equipment import RequiredEquipment
from app.server.timetabling.models.timeslot import Timeslot as ModelTimeslot
from app.server.timetabling.models.course import Course as ModelCourse
from app.server.timetabling.models.required_equipment import RequiredEquipment as ModelRequiredEquipment
from app.server.timetabling.models.classroom_equipment import ClassroomEquipment as ModelClassroomEquipment


class Timetabler():

    def __init__(self, project_id: int, user_id: int,
                 InitialSolver: Type[InitialBaseSolver],
                 Optimizer: Optional[Type[OptimizationBaseSolver]] = None):

        # Prepare classrooms
        classrooms = asyncio.run(Timetabler.prepare_classrooms(user_id=user_id))

        # Prepare classrooms
        timeslots = asyncio.run(Timetabler.prepare_timeslots(project_id=project_id, user_id=user_id))


        self.initial_solver = InitialSolver()
        self.initial_solver = InitialSolver()

    @staticmethod
    async def prepare_classrooms(user_id):
        async with async_session_maker() as session:
            statement = select(DatabaseClassroom).where(DatabaseClassroom.user == user_id)
            db_classrooms = (await session.execute(statement)).scalars().all()

            classrooms = [
                ModelClassroom(
                    id=db_classroom.id,
                    capacity=db_classroom.capacity,
                )
                for db_classroom in db_classrooms
            ]
            return classrooms

    @staticmethod
    async def prepare_timeslots(project_id, user_id):
        async with async_session_maker() as session:
            statement = select(DatabaseTimeslot)\
                .where(DatabaseTimeslot.user == user_id and DatabaseTimeslot.project == project_id)
            db_timeslots = (await session.execute(statement)).scalars().all()

            timeslots = [
                ModelTimeslot(
                    id=db_timeslot.id,
                    week=db_timeslot.week,
                    day=db_timeslot.day,
                    class_number=db_timeslot.class_number
                )
                for db_timeslot in db_timeslots
            ]
            return timeslots


    @staticmethod
    async def prepare_courses(project_id, user_id):
        async with async_session_maker() as session:
            statement = select(DatabaseCourse, Group, Discipline, Lecturer, CourseType, TimeInterval, ClassroomPool) \
                .join(Group, DatabaseCourse.group == Group.id) \
                .join(Discipline, DatabaseCourse.discipline == Discipline.id) \
                .join(Lecturer, DatabaseCourse.lecturer == Lecturer.id) \
                .join(CourseType, DatabaseCourse.course_type == CourseType.id) \
                .outerjoin(TimeInterval, DatabaseCourse.time_interval == TimeInterval.id) \
                .outerjoin(ClassroomPool, DatabaseCourse.classroom_pool == ClassroomPool.id) \
                .where(DatabaseCourse.user == user_id and DatabaseCourse.project == project_id)
            data = (await session.execute(statement)).scalars().all()

            statement = select(Course)

            for db_course, db_group, db_lecturer, db_course_type, db_time_interval, db_classroom_pool in data:
                pass


            classrooms = [
                ModelCourse(
                    id=db_classroom.id,
                    capacity=db_classroom.capacity,
                )
                for db_classroom in db_classrooms
            ]
            return classrooms


    def generate(self) -> (List[int], List[int], List[int]):
        pass
