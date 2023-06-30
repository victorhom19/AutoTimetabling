from strawberry.tools import create_type

from app.server.fastapi.graphql.types.Chain.ChainQuery import chain, chains
from app.server.fastapi.graphql.types.Classroom.ClassroomQuery import classroom, classrooms
from app.server.fastapi.graphql.types.ClassroomEquipment.ClassroomEquipmentQuery import classroom_equipment, classroom_equipments
from app.server.fastapi.graphql.types.ClassroomPool.ClassroomPoolQuery import classroom_pool, classroom_pools
from app.server.fastapi.graphql.types.ClassroomPoolClassroom.ClassroomPoolClassroomQuery import classroom_pool_classroom, classroom_pool_classrooms
from app.server.fastapi.graphql.types.ClassroomTimeSlot.ClassroomTimeSlotQuery import classroom_time_slot, classroom_time_slots
from app.server.fastapi.graphql.types.Combination.CombinationQuery import combination, combinations
from app.server.fastapi.graphql.types.Course.CourseQuery import course, courses
from app.server.fastapi.graphql.types.Department.DepartmentQuery import department, departments
from app.server.fastapi.graphql.types.Discipline.DisciplineQuery import discipline, disciplines
from app.server.fastapi.graphql.types.EducationBlock.EducationBlockQuery import education_block, education_blocks
from app.server.fastapi.graphql.types.EducationModule.EducationModuleQuery import education_module, education_modules
from app.server.fastapi.graphql.types.EducationProgram.EducationProgramQuery import education_program, education_programs
from app.server.fastapi.graphql.types.Group.GroupQuery import group, groups
from app.server.fastapi.graphql.types.Institution.InstitutionQuery import institution, institutions
from app.server.fastapi.graphql.types.Item.ItemQuery import item, items
from app.server.fastapi.graphql.types.Lecturer.LecturerQuery import lecturer, lecturers
from app.server.fastapi.graphql.types.Preference.PreferenceQuery import preference, preferences
from app.server.fastapi.graphql.types.Project.ProjectQuery import project, projects
from app.server.fastapi.graphql.types.RequiredEquipment.RequiredEquipmentQuery import required_equipment, required_equipments
from app.server.fastapi.graphql.types.TimeSlot.TimeSlotQuery import time_slot, time_slots
from app.server.fastapi.graphql.types.User.UserQuery import current_user


Query = create_type("Query", [
    chain, chains,
    classroom, classrooms,
    classroom_equipment, classroom_equipments,
    classroom_pool, classroom_pools,
    classroom_pool_classroom, classroom_pool_classrooms,
    classroom_time_slot, classroom_time_slots,
    combination, combinations,
    course, courses,
    department, departments,
    discipline, disciplines,
    education_block, education_blocks,
    education_module, education_modules,
    education_program, education_programs,
    group, groups,
    institution, institutions,
    item, items,
    lecturer, lecturers,
    preference, preferences,
    project, projects,
    required_equipment, required_equipments,
    time_slot, time_slots,
    current_user
])