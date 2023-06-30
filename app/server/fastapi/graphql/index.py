from typing import List, Optional

import strawberry
from fastapi import Depends
from strawberry.dataloader import DataLoader
from strawberry.fastapi import GraphQLRouter

from app.server.database.models import User as UserModel

from app.server.fastapi.dependencies import current_user
from app.server.fastapi.graphql.mutations import Mutations
from app.server.fastapi.graphql.query import Query
from app.server.fastapi.graphql.types.Chain.ChainSchema import ChainSchema, get_all_chains
from app.server.fastapi.graphql.types.Classroom.ClassroomSchema import ClassroomSchema, get_all_classrooms
from app.server.fastapi.graphql.types.ClassroomEquipment.ClassroomEquipmentSchema import ClassroomEquipmentSchema, get_all_classroom_equipments
from app.server.fastapi.graphql.types.ClassroomPool.ClassroomPoolSchema import ClassroomPoolSchema, get_all_classroom_pools
from app.server.fastapi.graphql.types.ClassroomPoolClassroom.ClassroomPoolClassroomSchema import ClassroomPoolClassroomSchema, get_all_classroom_pool_classrooms
from app.server.fastapi.graphql.types.ClassroomTimeSlot.ClassroomTimeSlotSchema import ClassroomTimeSlotSchema, get_all_classroom_time_slots
from app.server.fastapi.graphql.types.Combination.CombinationSchema import CombinationSchema, get_all_combinations
from app.server.fastapi.graphql.types.Course.CourseSchema import CourseSchema, get_all_courses
from app.server.fastapi.graphql.types.Department.DepartmentSchema import DepartmentSchema, get_all_departments
from app.server.fastapi.graphql.types.Discipline.DisciplineSchema import DisciplineSchema, get_all_disciplines
from app.server.fastapi.graphql.types.EducationBlock.EducationBlockSchema import EducationBlockSchema, get_all_education_blocks
from app.server.fastapi.graphql.types.EducationModule.EducationModuleSchema import EducationModuleSchema, get_all_education_modules
from app.server.fastapi.graphql.types.EducationProgram.EducationProgramSchema import EducationProgramSchema, get_all_education_programs
from app.server.fastapi.graphql.types.Group.GroupSchema import GroupSchema, get_all_groups
from app.server.fastapi.graphql.types.Institution.InstitutionSchema import InstitutionSchema, get_all_institutions
from app.server.fastapi.graphql.types.Item.ItemSchema import ItemSchema, get_all_items
from app.server.fastapi.graphql.types.Lecturer.LecturerSchema import LecturerSchema, get_all_lecturers
from app.server.fastapi.graphql.types.Preference.PreferenceSchema import PreferenceSchema, get_all_preferences
from app.server.fastapi.graphql.types.Project.ProjectSchema import ProjectSchema, get_all_projects
from app.server.fastapi.graphql.types.RequiredEquipment.RequiredEquipmentSchema import RequiredEquipmentSchema, get_all_required_equipments
from app.server.fastapi.graphql.types.TimeSlot.TimeSlotSchema import TimeSlotSchema, get_all_time_slots
from app.server.fastapi.graphql.types.User.UserSchema import UserSchema, get_all_users


# ----------------------------------- CHAIN LOADER FUNCTION ----------------------------------

async def load_chains(keys: List[int]) -> List[ChainSchema]:
    chains = await get_all_chains()

    def lookup(key: int) -> Optional[ChainSchema]:
        return next((chain for chain in chains if chain.id == key), None)

    return [lookup(key) for key in keys]


# --------------------------------- CLASSROOM LOADER FUNCTION --------------------------------

async def load_classrooms(keys: List[int]) -> List[ClassroomSchema]:
    classrooms = await get_all_classrooms()

    def lookup(key: int) -> Optional[ClassroomSchema]:
        return next((classroom for classroom in classrooms if classroom.id == key), None)

    return [lookup(key) for key in keys]


# ---------------------------- CLASSROOM EQUIPMENT LOADER FUNCTION ---------------------------

async def load_classroom_equipments(keys: List[int]) -> List[ClassroomEquipmentSchema]:
    classroom_equipments = await get_all_classroom_equipments()

    def lookup(key: int) -> Optional[ClassroomEquipmentSchema]:
        return next(
            (classroom_equipment for classroom_equipment in classroom_equipments if classroom_equipment.id == key),
            None)

    return [lookup(key) for key in keys]


# ------------------------------ CLASSROOM POOL LOADER FUNCTION ------------------------------

async def load_classroom_pools(keys: List[int]) -> List[ClassroomPoolSchema]:
    classroom_pools = await get_all_classroom_pools()

    def lookup(key: int) -> Optional[ClassroomPoolSchema]:
        return next((classroom_pool for classroom_pool in classroom_pools if classroom_pool.id == key), None)

    return [lookup(key) for key in keys]


# ------------------------- CLASSROOM POOL CLASSROOM LOADER FUNCTION -------------------------

async def load_classroom_pool_classrooms(keys: List[int]) -> List[ClassroomPoolClassroomSchema]:
    classroom_pool_classrooms = await get_all_classroom_pool_classrooms()

    def lookup(key: int) -> Optional[ClassroomPoolClassroomSchema]:
        return next((classroom_pool_classroom for classroom_pool_classroom in classroom_pool_classrooms if
                     classroom_pool_classroom.id == key), None)

    return [lookup(key) for key in keys]


# ---------------------------- CLASSROOM TIME SLOT LOADER FUNCTION ---------------------------

async def load_classroom_time_slots(keys: List[int]) -> List[ClassroomTimeSlotSchema]:
    classroom_time_slots = await get_all_classroom_time_slots()

    def lookup(key: int) -> Optional[ClassroomTimeSlotSchema]:
        return next((classroom_time_slot for classroom_time_slot in classroom_time_slots if
                     classroom_time_slot.id == key), None)

    return [lookup(key) for key in keys]


# -------------------------------- COMBINATION LOADER FUNCTION -------------------------------

async def load_combinations(keys: List[int]) -> List[CombinationSchema]:
    combinations = await get_all_combinations()

    def lookup(key: int) -> Optional[CombinationSchema]:
        return next((combination for combination in combinations if combination.id == key), None)

    return [lookup(key) for key in keys]


# ---------------------------------- COURSE LOADER FUNCTION ----------------------------------

async def load_courses(keys: List[int]) -> List[CourseSchema]:
    courses = await get_all_courses()

    def lookup(key: int) -> Optional[CourseSchema]:
        return next((course for course in courses if course.id == key), None)

    return [lookup(key) for key in keys]


# -------------------------------- DEPARTMENT LOADER FUNCTION --------------------------------

async def load_departments(keys: List[int]) -> List[DepartmentSchema]:
    departments = await get_all_departments()

    def lookup(key: int) -> Optional[DepartmentSchema]:
        return next((department for department in departments if department.id == key), None)

    return [lookup(key) for key in keys]


# -------------------------------- DISCIPLINE LOADER FUNCTION --------------------------------

async def load_disciplines(keys: List[int]) -> List[DisciplineSchema]:
    disciplines = await get_all_disciplines()

    def lookup(key: int) -> Optional[DisciplineSchema]:
        return next((discipline for discipline in disciplines if discipline.id == key), None)

    return [lookup(key) for key in keys]


# ------------------------------ EDUCATION BLOCK LOADER FUNCTION -----------------------------

async def load_education_blocks(keys: List[int]) -> List[EducationBlockSchema]:
    education_blocks = await get_all_education_blocks()

    def lookup(key: int) -> Optional[EducationBlockSchema]:
        return next((education_block for education_block in education_blocks if education_block.id == key), None)

    return [lookup(key) for key in keys]


# ----------------------------- EDUCATION MODULE LOADER FUNCTION -----------------------------

async def load_education_modules(keys: List[int]) -> List[EducationModuleSchema]:
    education_modules = await get_all_education_modules()

    def lookup(key: int) -> Optional[EducationModuleSchema]:
        return next((education_module for education_module in education_modules if education_module.id == key), None)

    return [lookup(key) for key in keys]


# ----------------------------- EDUCATION PROGRAM LOADER FUNCTION ----------------------------

async def load_education_programs(keys: List[int]) -> List[EducationProgramSchema]:
    education_programs = await get_all_education_programs()

    def lookup(key: int) -> Optional[EducationProgramSchema]:
        return next((education_program for education_program in education_programs if education_program.id == key),
                    None)

    return [lookup(key) for key in keys]


# ----------------------------------- GROUP LOADER FUNCTION ----------------------------------

async def load_groups(keys: List[int]) -> List[GroupSchema]:
    groups = await get_all_groups()

    def lookup(key: int) -> Optional[GroupSchema]:
        return next((group for group in groups if group.id == key), None)

    return [lookup(key) for key in keys]


# -------------------------------- INSTITUTION LOADER FUNCTION -------------------------------

async def load_institutions(keys: List[int]) -> List[InstitutionSchema]:
    institutions = await get_all_institutions()

    def lookup(key: int) -> Optional[InstitutionSchema]:
        return next((institution for institution in institutions if institution.id == key), None)

    return [lookup(key) for key in keys]


# ----------------------------------- ITEM LOADER FUNCTION -----------------------------------

async def load_items(keys: List[int]) -> List[ItemSchema]:
    items = await get_all_items()

    def lookup(key: int) -> Optional[ItemSchema]:
        return next((item for item in items if item.id == key), None)

    return [lookup(key) for key in keys]


# --------------------------------- LECTURER LOADER FUNCTION ---------------------------------

async def load_lecturers(keys: List[int]) -> List[LecturerSchema]:
    lecturers = await get_all_lecturers()

    def lookup(key: int) -> Optional[LecturerSchema]:
        return next((lecturer for lecturer in lecturers if lecturer.id == key), None)

    return [lookup(key) for key in keys]


# -------------------------------- PREFERENCE LOADER FUNCTION --------------------------------

async def load_preferences(keys: List[int]) -> List[PreferenceSchema]:
    preferences = await get_all_preferences()

    def lookup(key: int) -> Optional[PreferenceSchema]:
        return next((preference for preference in preferences if preference.id == key), None)

    return [lookup(key) for key in keys]


# ---------------------------------- PROJECT LOADER FUNCTION ---------------------------------

async def load_projects(keys: List[int]) -> List[ProjectSchema]:
    projects = await get_all_projects()

    def lookup(key: int) -> Optional[ProjectSchema]:
        return next((project for project in projects if project.id == key), None)

    return [lookup(key) for key in keys]


# ---------------------------- REQUIRED EQUIPMENT LOADER FUNCTION ----------------------------

async def load_required_equipments(keys: List[int]) -> List[RequiredEquipmentSchema]:
    required_equipments = await get_all_required_equipments()

    def lookup(key: int) -> Optional[RequiredEquipmentSchema]:
        return next((required_equipment for required_equipment in required_equipments if required_equipment.id == key),
                    None)

    return [lookup(key) for key in keys]


# --------------------------------- TIME SLOT LOADER FUNCTION --------------------------------

async def load_time_slots(keys: List[int]) -> List[TimeSlotSchema]:
    time_slots = await get_all_time_slots()

    def lookup(key: int) -> Optional[TimeSlotSchema]:
        return next((time_slot for time_slot in time_slots if time_slot.id == key), None)

    return [lookup(key) for key in keys]


# ----------------------------------- USER LOADER FUNCTION -----------------------------------

async def load_users(keys: List[int]) -> List[UserSchema]:
    users = await get_all_users()

    def lookup(key: int) -> Optional[UserSchema]:
        return next((user for user in users if user.id == key), None)

    return [lookup(key) for key in keys]


async def get_context(user: UserModel = Depends(current_user)):
    return {
        "current_user": user,

        "chain_loader": DataLoader(load_fn=load_chains),
        "classroom_loader": DataLoader(load_fn=load_classrooms),
        "classroom_equipment_loader": DataLoader(load_fn=load_classroom_equipments),
        "classroom_pool_loader": DataLoader(load_fn=load_classroom_pools),
        "classroom_pool_classroom_loader": DataLoader(load_fn=load_classroom_pool_classrooms),
        "combination_loader": DataLoader(load_fn=load_combinations),
        "course_loader": DataLoader(load_fn=load_courses),
        "department_loader": DataLoader(load_fn=load_departments),
        "discipline_loader": DataLoader(load_fn=load_disciplines),
        "education_block_loader": DataLoader(load_fn=load_education_blocks),
        "education_module_loader": DataLoader(load_fn=load_education_modules),
        "education_program_loader": DataLoader(load_fn=load_education_programs),
        "group_loader": DataLoader(load_fn=load_groups),
        "institution_loader": DataLoader(load_fn=load_institutions),
        "item_loader": DataLoader(load_fn=load_items),
        "lecturer_loader": DataLoader(load_fn=load_lecturers),
        "preference_loader": DataLoader(load_fn=load_preferences),
        "project_loader": DataLoader(load_fn=load_projects),
        "required_equipment_loader": DataLoader(load_fn=load_required_equipments),
        "time_slot_loader": DataLoader(load_fn=load_time_slots),
        "user_loader": DataLoader(load_fn=load_users)
    }

schema = strawberry.Schema(Query, Mutations)

graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context
)
