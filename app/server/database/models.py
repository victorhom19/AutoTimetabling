import enum

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, Identity, String, ForeignKey, Boolean, Enum
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'user'

    id = Column('id', Integer, Identity(start=1, increment=1), primary_key=True)
    username = Column('username', String, nullable=False)
    email = Column('email', String, nullable=False)


class Project(Base):
    __tablename__ = 'project'

    id = Column('id', Integer, Identity(start=1, increment=1), primary_key=True)
    user = Column('user', Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    name = Column('name', String, nullable=False)
    description = Column('description', String, nullable=True)


class Item(Base):
    __tablename__ = 'item'

    id = Column('id', Integer, Identity(start=1, increment=1), primary_key=True)
    user = Column('user', Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    name = Column('name', String, nullable=False)
    description = Column('description', String, nullable=True)


class Institution(Base):
    __tablename__ = 'institution'

    id = Column('id', Integer, Identity(start=1, increment=1), primary_key=True)
    user = Column('user', Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    code = Column('code', Integer, nullable=False)
    name = Column('name', String, nullable=False)


class Classroom(Base):
    __tablename__ = 'classroom'

    id = Column('id', Integer, Identity(start=1, increment=1), primary_key=True)
    user = Column('user', Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    building = Column('building', String, nullable=False)
    auditory_number = Column('auditory_number', String, nullable=False)
    capacity = Column('capacity', Integer, nullable=False)


class ClassroomPool(Base):
    __tablename__ = 'classroom_pool'
    id = Column('id', Integer, Identity(start=1, increment=1), primary_key=True)
    user = Column('user', Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    name = Column('name', String, nullable=True)
    color = Column('color', String, nullable=True)


class Combination(Base):
    __tablename__ = 'combination'

    id = Column('id', Integer, Identity(start=1, increment=1), primary_key=True)
    project = Column('project', Integer, ForeignKey('project.id', ondelete='CASCADE'), nullable=False)
    user = Column('user', Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    name = Column('name', String, nullable=True)
    color = Column('color', String, nullable=True)


class Chain(Base):
    __tablename__ = 'chain'

    id = Column('id', Integer, Identity(start=1, increment=1), primary_key=True)
    project = Column('project', Integer, ForeignKey('project.id', ondelete='CASCADE'), nullable=False)
    user = Column('user', Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    name = Column('name', String, nullable=True)
    color = Column('color', String, nullable=True)


class ClassroomEquipment(Base):
    __tablename__ = 'classroom_equipment'

    id = Column('id', Integer, Identity(start=1, increment=1), primary_key=True)
    user = Column('user', Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    classroom = Column('classroom', Integer, ForeignKey('classroom.id', ondelete='CASCADE'), nullable=False)
    item = Column('item', Integer, ForeignKey('item.id', ondelete='CASCADE'), nullable=False)
    amount = Column('amount', Integer, nullable=False)


class Department(Base):
    __tablename__ = 'department'

    id = Column('id', Integer, Identity(start=1, increment=1), primary_key=True)
    user = Column('user', Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    institution = Column('institution', Integer, ForeignKey('institution.id', ondelete='CASCADE'))
    name = Column('name', String, nullable=False)


class EducationProgram(Base):
    __tablename__ = 'education_program'

    class EducationLevel(enum.Enum):
        BACHELOR = 0
        MASTER = 1
        SPECIALIST = 2
        POSTGRADUATE = 3

    id = Column('id', Integer, Identity(start=1, increment=1), primary_key=True)
    user = Column('user', Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    code = Column('code', String, nullable=False)
    name = Column('name', String, nullable=False)
    profile_code = Column('profile_code', String, nullable=False)
    profile_name = Column('profile_name', String, nullable=False)
    education_level = Column('education_level', Enum(EducationLevel), nullable=False)


class ClassroomPoolClassroom(Base):
    __tablename__ = 'classroom_pool_classroom'

    id = Column('id', Integer, Identity(start=1, increment=1), primary_key=True)
    user = Column('user', Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    classroom_pool = Column('classroom_pool', Integer, ForeignKey('classroom_pool.id', ondelete='CASCADE'), nullable=False)
    classroom = Column('classroom', Integer, ForeignKey('classroom.id', ondelete='CASCADE'), nullable=False)


class TimeSlot(Base):
    __tablename__ = 'time_slot'

    class TimeSlotType(enum.Enum):
        DEFAULT = 0
        WEEKLY = 1

    id = Column('id', Integer, Identity(start=1, increment=1), primary_key=True)
    project = Column('project', Integer, ForeignKey('project.id', ondelete='CASCADE'), nullable=False)
    user = Column('user', Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    time_slot_type = Column('time_slot_type', Enum(TimeSlotType), nullable=False)
    week = Column('week', Integer, nullable=False)
    day = Column('day', Integer, nullable=False)
    class_number = Column('class_number', Integer, nullable=False)


class ClassroomTimeSlot(Base):
    __tablename__ = 'classroom_time_slot'

    id = Column('id', Integer, Identity(start=1, increment=1), primary_key=True)
    classroom = Column('classroom', Integer, ForeignKey('classroom.id', ondelete='CASCADE'), nullable=False)
    time_slot = Column('time_slot', Integer, ForeignKey('time_slot.id', ondelete='CASCADE'), nullable=False)


class Lecturer(Base):
    __tablename__ = 'lecturer'

    id = Column('id', Integer, Identity(start=1, increment=1), primary_key=True)
    user = Column('user', Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    department = Column('department', Integer, ForeignKey('department.id', ondelete='CASCADE'), nullable=False)
    name = Column('name', String, nullable=False)
    email = Column('email', String, nullable=True)


class EducationBlock(Base):
    __tablename__ = 'education_block'

    id = Column('id', Integer, Identity(start=1, increment=1), primary_key=True)
    user = Column('user', Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    name = Column('name', String, nullable=False)
    code = Column('code', String, nullable=False)
    education_program = Column('education_program', Integer, ForeignKey('education_program.id', ondelete='CASCADE'), nullable=False)


class Group(Base):
    __tablename__ = 'group'

    id = Column('id', Integer, Identity(start=1, increment=1), primary_key=True)
    user = Column('user', Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    code = Column('code', String, nullable=False)
    department = Column('department', Integer, ForeignKey('department.id', ondelete='CASCADE'), nullable=False)
    education_program = Column('education_program', Integer, ForeignKey('education_program.id', ondelete='CASCADE'), nullable=False)
    size = Column('size', Integer, nullable=False)
    part_of = Column('part_of', ForeignKey('group.id', ondelete='CASCADE'), nullable=True)


class EducationModule(Base):
    __tablename__ = 'education_module'

    id = Column('id', Integer, Identity(start=1, increment=1), primary_key=True)
    user = Column('user', Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    name = Column('name', String, nullable=False)
    code = Column('code', String, nullable=False)
    is_base_module = Column('is_base_module', Boolean, nullable=False)
    education_block = Column('education_block', ForeignKey('education_block.id', ondelete='CASCADE'), nullable=False)
    parent_module = Column('parent_module', ForeignKey('education_module.id', ondelete='CASCADE'), nullable=True)


class Discipline(Base):
    __tablename__ = 'discipline'

    class Assessment(enum.Enum):
        EXAM = 0
        ASSESSMENT = 1
        ASSESSMENT_WITH_GRADE = 2
        COURSE_PROJECT = 3
        COURSE_WORK = 4
        VERIFICATION_WORK = 5
        GRADE = 6
        GRAPHIC_WORK = 7

    id = Column('id', Integer, Identity(start=1, increment=1), primary_key=True)
    name = Column('name', String, nullable=False)
    education_module = Column('education_module', Integer, ForeignKey('education_module.id', ondelete='CASCADE'), nullable=False)
    assessment = Column('assessment', Enum(Assessment), nullable=False)


class RequiredEquipment(Base):
    __tablename__ = 'required_equipment'

    id = Column('id', Integer, Identity(start=1, increment=1), primary_key=True)
    user = Column('user', Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    discipline = Column('discipline', Integer, ForeignKey('discipline.id', ondelete='CASCADE'), nullable=False)
    item = Column('item', Integer, ForeignKey('item.id', ondelete='CASCADE'), nullable=False)
    amount = Column('amount', Integer, nullable=False)


class Course(Base):
    __tablename__ = 'course'

    class CourseType(enum.Enum):
        LECTURE = 0
        PRACTICE = 1
        LABORATORY = 2

    id = Column('id', Integer, Identity(start=1, increment=1), primary_key=True)
    project = Column('project', Integer, ForeignKey("project.id", ondelete='CASCADE'), nullable=False)
    user = Column('user', Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    discipline = Column('discipline', Integer, ForeignKey('discipline.id', ondelete='CASCADE'), nullable=False)
    lecturer = Column('lecturer', Integer, ForeignKey('lecturer.id', ondelete='CASCADE'), nullable=False)
    group = Column('group', Integer, ForeignKey('group.id', ondelete='CASCADE'), nullable=False)
    course_type = Column('course_type', Enum(CourseType), nullable=False)
    duration = Column('duration', Integer, nullable=False)
    week_intensity = Column('week_intensity', Integer, nullable=False)
    block_length = Column('block_length', Integer, nullable=False)
    time_slot_from = Column('time_slot_from', Integer, ForeignKey('time_slot.id', ondelete='SET NULL'), nullable=True)
    time_slot_to = Column('time_slot_to', Integer, ForeignKey('time_slot.id', ondelete='SET NULL'), nullable=True)
    classroom_pool = Column('classroom_pool', ForeignKey('classroom_pool.id', ondelete='SET NULL'), nullable=True)
    combination = Column('combination', ForeignKey('combination.id', ondelete='SET NULL'), nullable=True)
    chain = Column('chain', ForeignKey('chain.id', ondelete='SET NULL'), nullable=True)
    chain_priority = Column('chain_priority', Integer, nullable=True)


class Preference(Base):
    __tablename__ = 'preference'

    id = Column('id', Integer, Identity(start=1, increment=1), primary_key=True)
    project = Column('project', Integer, ForeignKey("project.id", ondelete='CASCADE'), nullable=False)
    user = Column('user', Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    lecturer = Column('lecturer', Integer, ForeignKey("lecturer.id", ondelete='CASCADE'), nullable=False)
    time_slot = Column('time_slot', Integer, ForeignKey('time_slot.id', ondelete='CASCADE'), nullable=False)
    value = Column('value', Integer, nullable=False)



