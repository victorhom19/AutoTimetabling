from strawberry.tools import create_type

from app.server.fastapi.graphql.types.Chain.ChainMutations import create_chain, update_chain, delete_chain
from app.server.fastapi.graphql.types.Classroom.ClassroomMutations import create_classroom, update_classroom, delete_classroom
from app.server.fastapi.graphql.types.ClassroomEquipment.ClassroomEquipmentMutations import create_classroom_equipment, update_classroom_equipment, delete_classroom_equipment
from app.server.fastapi.graphql.types.ClassroomPool.ClassroomPoolMutations import create_classroom_pool, update_classroom_pool, delete_classroom_pool
from app.server.fastapi.graphql.types.ClassroomPoolClassroom.ClassroomPoolClassroomMutations import create_classroom_pool_classroom, update_classroom_pool_classroom, delete_classroom_pool_classroom
from app.server.fastapi.graphql.types.ClassroomTimeSlot.ClassroomTimeSlotMutations import create_classroom_time_slot, update_classroom_time_slot, delete_classroom_time_slot
from app.server.fastapi.graphql.types.Combination.CombinationMutations import create_combination, update_combination, delete_combination
from app.server.fastapi.graphql.types.Course.CourseMutations import create_course, update_course, delete_course
from app.server.fastapi.graphql.types.Department.DepartmentMutations import create_department, update_department, delete_department
from app.server.fastapi.graphql.types.Discipline.DisciplineMutations import create_discipline, update_discipline, delete_discipline
from app.server.fastapi.graphql.types.EducationBlock.EducationBlockMutations import create_education_block, update_education_block, delete_education_block
from app.server.fastapi.graphql.types.EducationModule.EducationModuleMutations import create_education_module, update_education_module, delete_education_module
from app.server.fastapi.graphql.types.EducationProgram.EducationProgramMutations import create_education_program, update_education_program, delete_education_program
from app.server.fastapi.graphql.types.Group.GroupMutations import create_group, update_group, delete_group
from app.server.fastapi.graphql.types.Institution.InstitutionMutations import create_institution, update_institution, delete_institution
from app.server.fastapi.graphql.types.Item.ItemMutations import create_item, update_item, delete_item
from app.server.fastapi.graphql.types.Lecturer.LecturerMutations import create_lecturer, update_lecturer, delete_lecturer
from app.server.fastapi.graphql.types.Preference.PreferenceMutations import create_preference, update_preference, delete_preference
from app.server.fastapi.graphql.types.Project.ProjectMutations import create_project, update_project, delete_project
from app.server.fastapi.graphql.types.RequiredEquipment.RequiredEquipmentMutations import create_required_equipment, update_required_equipment, delete_required_equipment
from app.server.fastapi.graphql.types.TimeSlot.TimeSlotMutations import create_time_slot, update_time_slot, delete_time_slot


Mutations = create_type("Mutations", [
   create_chain, update_chain, delete_chain,
   create_classroom, update_classroom, delete_classroom,
   create_classroom_equipment, update_classroom_equipment, delete_classroom_equipment,
   create_classroom_pool, update_classroom_pool, delete_classroom_pool,
   create_classroom_pool_classroom, update_classroom_pool_classroom, delete_classroom_pool_classroom,
   create_classroom_time_slot, update_classroom_time_slot, delete_classroom_time_slot,
   create_combination, update_combination, delete_combination,
   create_course, update_course, delete_course,
   create_department, update_department, delete_department,
   create_discipline, update_discipline, delete_discipline,
   create_education_block, update_education_block, delete_education_block,
   create_education_module, update_education_module, delete_education_module,
   create_education_program, update_education_program, delete_education_program,
   create_group, update_group, delete_group,
   create_institution, update_institution, delete_institution,
   create_item, update_item, delete_item,
   create_lecturer, update_lecturer, delete_lecturer,
   create_preference, update_preference, delete_preference,
   create_project, update_project, delete_project,
   create_required_equipment, update_required_equipment, delete_required_equipment,
   create_time_slot, update_time_slot, delete_time_slot,
])