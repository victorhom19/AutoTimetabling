from app.server.timetabling.models.classroom import Classroom
from app.server.timetabling.models.classroom_equipment import ClassroomEquipment
from app.server.timetabling.models.course import Course
from app.server.timetabling.models.required_equipment import RequiredEquipment
from app.server.timetabling.models.timeslot import CPD, DPW, Timeslot

course_params = {
    'type': 0,
    'group_size': 20,
    'part_of': None,
    'duration': 2,
    'week_intensity': 1,
    'timeslot_from': None,
    'timeslot_to': None,
    'chain_code': None,
    'chain_priority': None,


}

courses = [
    # 90101

    # Защита информации лекции
    Course(id=3, discipline=4, lecturer=4, group=0, combined_code=1, block_length=1, valid_classrooms=None, **course_params),
    # Защита информации практика
    Course(id=4, discipline=4, lecturer=4, group=0, combined_code=None, block_length=2, valid_classrooms=[3], **course_params),

    # Системный анализ и принятие решений лекции
    Course(id=5, discipline=3, lecturer=3, group=0, combined_code=2, block_length=1, valid_classrooms=None, **course_params),
    # Системный анализ и принятие решений практика
    Course(id=6, discipline=5, lecturer=5, group=0, combined_code=None, block_length=1, valid_classrooms=None, **course_params),

    # Разработка сетевых приложений практика
    Course(id=7, discipline=2, lecturer=2, group=0, combined_code=None, block_length=1, valid_classrooms=None, **course_params),


    # 90201

    # Тестирование ПО лекции
    Course(id=8, discipline=1, lecturer=1, group=1, combined_code=0, block_length=1, valid_classrooms=None,
           **course_params),
    # Тестирование ПО практики
    Course(id=9, discipline=1, lecturer=1, group=1, combined_code=None, block_length=2, valid_classrooms=None,
           **course_params),

    # Защита информации лекции
    Course(id=10, discipline=4, lecturer=4, group=1, combined_code=1, block_length=1, valid_classrooms=None,
           **course_params),
    # Защита информации практика
    Course(id=11, discipline=4, lecturer=4, group=1, combined_code=None, block_length=2, valid_classrooms=[3],
           **course_params),

    # Системный анализ и принятие решений лекции
    Course(id=12, discipline=3, lecturer=4, group=2, combined_code=2, block_length=1, valid_classrooms=None,
           **course_params),
    # Системный анализ и принятие решений практика
    Course(id=13, discipline=3, lecturer=3, group=2, combined_code=None, block_length=1, valid_classrooms=None,
           **course_params),

    # Разработка сетевых приложений практика
    Course(id=14, discipline=2, lecturer=2, group=2, combined_code=None, block_length=1, valid_classrooms=None,
           **course_params),

    # 90202

    # Тестирование ПО лекции
    Course(id=15, discipline=1, lecturer=1, group=3, combined_code=0, block_length=1, valid_classrooms=None,
           **course_params),
    # Тестирование ПО практики
    Course(id=16, discipline=1, lecturer=1, group=3, combined_code=None, block_length=2, valid_classrooms=None,
           **course_params),

    # Защита информации лекции
    Course(id=17, discipline=4, lecturer=4, group=3, combined_code=1, block_length=1, valid_classrooms=None,
           **course_params),
    # Защита информации практика
    Course(id=18, discipline=4, lecturer=4, group=3, combined_code=None, block_length=2, valid_classrooms=[3],
           **course_params),

    # Системный анализ и принятие решений лекции
    Course(id=19, discipline=3, lecturer=3, group=3, combined_code=2, block_length=1, valid_classrooms=None,
           **course_params),
    # Системный анализ и принятие решений практика
    Course(id=20, discipline=5, lecturer=3, group=3, combined_code=None, block_length=1, valid_classrooms=None,
           **course_params),

    # Разработка сетевых приложений практика
    Course(id=21, discipline=2, lecturer=2, group=3, combined_code=None, block_length=1, valid_classrooms=None,
           **course_params),

    # 90203

    # Тестирование ПО лекции
    Course(id=22, discipline=1, lecturer=1, group=4, combined_code=0, block_length=1, valid_classrooms=None,
           **course_params),
    # Тестирование ПО практики
    Course(id=23, discipline=1, lecturer=1, group=4, combined_code=None, block_length=2, valid_classrooms=None,
           **course_params),

    # Защита информации лекции
    Course(id=24, discipline=4, lecturer=4, group=4, combined_code=1, block_length=1, valid_classrooms=None,
           **course_params),
    # Защита информации практика
    Course(id=25, discipline=4, lecturer=4, group=4, combined_code=None, block_length=2, valid_classrooms=[3],
           **course_params),

    # Системный анализ и принятие решений лекции
    Course(id=26, discipline=3, lecturer=3, group=4, combined_code=2, block_length=1, valid_classrooms=None,
           **course_params),
    # Системный анализ и принятие решений практика
    Course(id=27, discipline=5, lecturer=3, group=4, combined_code=None, block_length=1, valid_classrooms=None,
           **course_params),

    # Разработка сетевых приложений практика
    Course(id=28, discipline=2, lecturer=2, group=4, combined_code=None, block_length=1, valid_classrooms=None,
           **course_params),
]

classrooms = [
    Classroom(id=1, capacity=80),
    Classroom(id=2, capacity=110),
    Classroom(id=3, capacity=24),
    Classroom(id=4, capacity=24),
    Classroom(id=5, capacity=24),
]

timeslots = [
    Timeslot(
        id=w*36 + d*6 + c,
        week=w,
        day=d,
        class_number=c
    )
    for w in range(2) for d in range(DPW) for c in range(CPD)
]

classroom_equipment = []

required_equipment = []
