from app.server.timetabling.models.classroom import Classroom
from app.server.timetabling.models.classroom_equipment import ClassroomEquipment
from app.server.timetabling.models.course import Course
from app.server.timetabling.models.required_equipment import RequiredEquipment
from app.server.timetabling.models.timeslot import CPD, DPW, Timeslot

course_params = {
    'type': 0,
    'group_size': 30,
    'combined_code': None,
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
    Course(id=0, discipline=0, lecturer=0, group=1, part_of=0, **course_params),
    Course(id=1, discipline=1, lecturer=1, group=2, part_of=0, **course_params),
    Course(id=2, discipline=2, lecturer=2, group=1, part_of=0, **course_params),
    Course(id=3, discipline=3, lecturer=3, group=2, part_of=0, **course_params),
    Course(id=4, discipline=4, lecturer=4, group=1, part_of=0, **course_params),
    Course(id=5, discipline=5, lecturer=5, group=2, part_of=0, **course_params),
    Course(id=6, discipline=6, lecturer=6, group=1, part_of=0, **course_params),
    Course(id=7, discipline=7, lecturer=7, group=2, part_of=0, **course_params),
    Course(id=8, discipline=8, lecturer=8, group=1, part_of=0, **course_params),
    Course(id=9, discipline=9, lecturer=9, group=2, part_of=0, **course_params),
    Course(id=10, discipline=10, lecturer=10, group=1, part_of=0, **course_params),
    Course(id=11, discipline=11, lecturer=11, group=2, part_of=0, **course_params),
]

classrooms = [
    Classroom(id=i, capacity=30)
    for i in range(2)
]

timeslots = [
    Timeslot(
        id=c,
        week=w,
        day=d,
        class_number=c
    )
    for w in range(1) for d in range(1) for c in range(CPD)
]

classroom_equipment = []

required_equipment = []
