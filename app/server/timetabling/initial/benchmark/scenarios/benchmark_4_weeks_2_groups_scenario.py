from app.server.timetabling.models.classroom import Classroom
from app.server.timetabling.models.classroom_equipment import ClassroomEquipment
from app.server.timetabling.models.course import Course
from app.server.timetabling.models.required_equipment import RequiredEquipment
from app.server.timetabling.models.timeslot import CPD, DPW, Timeslot

course_params = {
    'type': 0,
    'group_size': 30,
    'part_of': None,
    'duration': 4,
    'week_intensity': 1,
    'block_length': 1,
    'timeslot_from': None,
    'timeslot_to': None,
    'chain_code': None,
    'chain_priority': None,
    'valid_classrooms': None,


}

courses = [
    # Группа 0
    Course(id=0, discipline=0, lecturer=0, group=0, combined_code=0, **course_params),
    Course(id=1, discipline=0, lecturer=0, group=0, combined_code=None, **course_params),
    Course(id=2, discipline=1, lecturer=1, group=0, combined_code=1, **course_params),
    Course(id=3, discipline=1, lecturer=1, group=0, combined_code=None, **course_params),
    Course(id=4, discipline=2, lecturer=2, group=0, combined_code=2, **course_params),
    Course(id=5, discipline=2, lecturer=2, group=0, combined_code=None, **course_params),
    Course(id=6, discipline=3, lecturer=3, group=0, combined_code=3, **course_params),
    Course(id=7, discipline=3, lecturer=3, group=0, combined_code=None, **course_params),
    Course(id=8, discipline=4, lecturer=4, group=0, combined_code=4, **course_params),
    Course(id=9, discipline=4, lecturer=4, group=0, combined_code=None, **course_params),

    # Группа 0
    Course(id=10, discipline=0, lecturer=0, group=1, combined_code=0, **course_params),
    Course(id=11, discipline=0, lecturer=0, group=1, combined_code=None, **course_params),
    Course(id=12, discipline=1, lecturer=1, group=1, combined_code=1, **course_params),
    Course(id=13, discipline=1, lecturer=1, group=1, combined_code=None, **course_params),
    Course(id=14, discipline=2, lecturer=2, group=1, combined_code=2, **course_params),
    Course(id=15, discipline=2, lecturer=2, group=1, combined_code=None, **course_params),
    Course(id=16, discipline=3, lecturer=3, group=1, combined_code=3, **course_params),
    Course(id=17, discipline=3, lecturer=3, group=1, combined_code=None, **course_params),
    Course(id=18, discipline=4, lecturer=4, group=1, combined_code=4, **course_params),
    Course(id=19, discipline=4, lecturer=4, group=1, combined_code=None, **course_params),
]

classrooms = [
    Classroom(id=0, capacity=30),
    Classroom(id=1, capacity=30),
    Classroom(id=2, capacity=60),
]

timeslots = [
    Timeslot(
        id=w * DPW * CPD + d * CPD + c,
        week=w,
        day=d,
        class_number=c
    )
    for w in range(4) for d in range(DPW) for c in range(CPD)
]

classroom_equipment = []

required_equipment = []
