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
    'chain_code': 0,
    'valid_classrooms': None,


}

courses = [
    Course(id=0, discipline=0, lecturer=0, group=0, chain_priority=5, **course_params),
    Course(id=1, discipline=1, lecturer=1, group=1, chain_priority=4, **course_params),
    Course(id=2, discipline=2, lecturer=2, group=2, chain_priority=3, **course_params),
    Course(id=3, discipline=3, lecturer=3, group=3, chain_priority=2, **course_params),
    Course(id=4, discipline=4, lecturer=4, group=4, chain_priority=1, **course_params),
    Course(id=5, discipline=5, lecturer=5, group=5, chain_priority=0, **course_params),
]

classrooms = [
    Classroom(id=0, capacity=30)
    for i in range(CPD)
]

timeslots = [
    Timeslot(
        id=c,
        week=w,
        day=d,
        class_number=c
    )
    for w in range(1) for d in range(1) for c in range(3*CPD)
]

classroom_equipment = []

required_equipment = []
