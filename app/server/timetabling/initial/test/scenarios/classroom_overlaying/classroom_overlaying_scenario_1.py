from app.server.timetabling.models.classroom import Classroom
from app.server.timetabling.models.classroom_equipment import ClassroomEquipment
from app.server.timetabling.models.course import Course
from app.server.timetabling.models.required_equipment import RequiredEquipment
from app.server.timetabling.models.timeslot import CPD, DPW, Timeslot

course_params = {
    'type': 0,
    'group_size': 30,
    'combined_code': None,
    'part_of': None,
    'duration': 1,
    'week_intensity': 1,
    'block_length': 1,
    'timeslot_from': None,
    'timeslot_to': None,
    'chain_code': None,
    'chain_priority': None,
    'valid_classrooms': None,


}

courses = [
    Course(id=i, discipline=i, lecturer=i, group=i, **course_params)
    for i in range(2*CPD)
]

classrooms = [
    Classroom(id=i, capacity=30)
    for i in range(2)
]

timeslots = [
    Timeslot(
        id=w * DPW * CPD + d * CPD + c,
        week=w,
        day=d,
        class_number=c
    )
    for w in range(1) for d in range(1) for c in range(CPD)
]

classroom_equipment = []

required_equipment = []
