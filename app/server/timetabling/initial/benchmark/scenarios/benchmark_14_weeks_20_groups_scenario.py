from app.server.timetabling.models.classroom import Classroom
from app.server.timetabling.models.classroom_equipment import ClassroomEquipment
from app.server.timetabling.models.course import Course
from app.server.timetabling.models.required_equipment import RequiredEquipment
from app.server.timetabling.models.timeslot import CPD, DPW, Timeslot

course_params = {
    'type': 0,
    'group_size': 30,
    'part_of': None,
    'duration': 14,
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
    Course(id=2, discipline=1, lecturer=3, group=0, combined_code=1, **course_params),
    Course(id=3, discipline=1, lecturer=3, group=0, combined_code=None, **course_params),
    Course(id=4, discipline=2, lecturer=6, group=0, combined_code=2, **course_params),
    Course(id=5, discipline=2, lecturer=6, group=0, combined_code=None, **course_params),
    Course(id=6, discipline=3, lecturer=9, group=0, combined_code=3, **course_params),
    Course(id=7, discipline=3, lecturer=9, group=0, combined_code=None, **course_params),
    Course(id=8, discipline=4, lecturer=12, group=0, combined_code=4, **course_params),
    Course(id=9, discipline=4, lecturer=12, group=0, combined_code=None, **course_params),

    # Группа 1
    Course(id=10, discipline=0, lecturer=0, group=1, combined_code=0, **course_params),
    Course(id=11, discipline=0, lecturer=1, group=1, combined_code=None, **course_params),
    Course(id=12, discipline=1, lecturer=3, group=1, combined_code=1, **course_params),
    Course(id=13, discipline=1, lecturer=4, group=1, combined_code=None, **course_params),
    Course(id=14, discipline=2, lecturer=6, group=1, combined_code=2, **course_params),
    Course(id=15, discipline=2, lecturer=7, group=1, combined_code=None, **course_params),
    Course(id=16, discipline=3, lecturer=9, group=1, combined_code=3, **course_params),
    Course(id=17, discipline=3, lecturer=10, group=1, combined_code=None, **course_params),
    Course(id=18, discipline=4, lecturer=12, group=1, combined_code=4, **course_params),
    Course(id=19, discipline=4, lecturer=13, group=1, combined_code=None, **course_params),

    # Группа 2
    Course(id=20, discipline=0, lecturer=0, group=2, combined_code=0, **course_params),
    Course(id=21, discipline=0, lecturer=1, group=2, combined_code=None, **course_params),
    Course(id=22, discipline=1, lecturer=3, group=2, combined_code=1, **course_params),
    Course(id=23, discipline=1, lecturer=4, group=2, combined_code=None, **course_params),
    Course(id=24, discipline=2, lecturer=6, group=2, combined_code=2, **course_params),
    Course(id=25, discipline=2, lecturer=7, group=2, combined_code=None, **course_params),
    Course(id=26, discipline=3, lecturer=9, group=2, combined_code=3, **course_params),
    Course(id=27, discipline=3, lecturer=10, group=2, combined_code=None, **course_params),
    Course(id=28, discipline=4, lecturer=12, group=2, combined_code=4, **course_params),
    Course(id=29, discipline=4, lecturer=13, group=2, combined_code=None, **course_params),

    # Группа 3
    Course(id=30, discipline=0, lecturer=0, group=3, combined_code=0, **course_params),
    Course(id=31, discipline=0, lecturer=2, group=3, combined_code=None, **course_params),
    Course(id=32, discipline=1, lecturer=3, group=3, combined_code=1, **course_params),
    Course(id=33, discipline=1, lecturer=5, group=3, combined_code=None, **course_params),
    Course(id=34, discipline=2, lecturer=6, group=3, combined_code=2, **course_params),
    Course(id=35, discipline=2, lecturer=8, group=3, combined_code=None, **course_params),
    Course(id=36, discipline=3, lecturer=9, group=3, combined_code=3, **course_params),
    Course(id=37, discipline=3, lecturer=11, group=3, combined_code=None, **course_params),
    Course(id=38, discipline=4, lecturer=12, group=3, combined_code=4, **course_params),
    Course(id=39, discipline=4, lecturer=14, group=3, combined_code=None, **course_params),

    # Группа 4
    Course(id=40, discipline=0, lecturer=0, group=4, combined_code=0, **course_params),
    Course(id=41, discipline=0, lecturer=2, group=4, combined_code=None, **course_params),
    Course(id=42, discipline=1, lecturer=3, group=4, combined_code=1, **course_params),
    Course(id=43, discipline=1, lecturer=5, group=4, combined_code=None, **course_params),
    Course(id=44, discipline=2, lecturer=6, group=4, combined_code=2, **course_params),
    Course(id=45, discipline=2, lecturer=8, group=4, combined_code=None, **course_params),
    Course(id=46, discipline=3, lecturer=9, group=4, combined_code=3, **course_params),
    Course(id=47, discipline=3, lecturer=11, group=4, combined_code=None, **course_params),
    Course(id=48, discipline=4, lecturer=12, group=4, combined_code=4, **course_params),
    Course(id=49, discipline=4, lecturer=14, group=4, combined_code=None, **course_params),


    # Группа 5
    Course(id=50, discipline=5, lecturer=15, group=5, combined_code=5, **course_params),
    Course(id=51, discipline=5, lecturer=15, group=5, combined_code=None, **course_params),
    Course(id=52, discipline=6, lecturer=18, group=5, combined_code=6, **course_params),
    Course(id=53, discipline=6, lecturer=18, group=5, combined_code=None, **course_params),
    Course(id=54, discipline=7, lecturer=21, group=5, combined_code=7, **course_params),
    Course(id=55, discipline=7, lecturer=21, group=5, combined_code=None, **course_params),
    Course(id=56, discipline=8, lecturer=24, group=5, combined_code=8, **course_params),
    Course(id=57, discipline=8, lecturer=24, group=5, combined_code=None, **course_params),
    Course(id=58, discipline=9, lecturer=27, group=5, combined_code=9, **course_params),
    Course(id=59, discipline=9, lecturer=27, group=5, combined_code=None, **course_params),

    # Группа 6
    Course(id=60, discipline=5, lecturer=15, group=6, combined_code=5, **course_params),
    Course(id=61, discipline=5, lecturer=16, group=6, combined_code=None, **course_params),
    Course(id=62, discipline=6, lecturer=18, group=6, combined_code=6, **course_params),
    Course(id=63, discipline=6, lecturer=19, group=6, combined_code=None, **course_params),
    Course(id=64, discipline=7, lecturer=21, group=6, combined_code=7, **course_params),
    Course(id=65, discipline=7, lecturer=22, group=6, combined_code=None, **course_params),
    Course(id=66, discipline=8, lecturer=24, group=6, combined_code=8, **course_params),
    Course(id=67, discipline=8, lecturer=25, group=6, combined_code=None, **course_params),
    Course(id=68, discipline=9, lecturer=27, group=6, combined_code=9, **course_params),
    Course(id=69, discipline=9, lecturer=28, group=6, combined_code=None, **course_params),

    # Группа 7
    Course(id=70, discipline=5, lecturer=15, group=7, combined_code=5, **course_params),
    Course(id=71, discipline=5, lecturer=16, group=7, combined_code=None, **course_params),
    Course(id=72, discipline=6, lecturer=18, group=7, combined_code=6, **course_params),
    Course(id=73, discipline=6, lecturer=19, group=7, combined_code=None, **course_params),
    Course(id=74, discipline=7, lecturer=21, group=7, combined_code=7, **course_params),
    Course(id=75, discipline=7, lecturer=22, group=7, combined_code=None, **course_params),
    Course(id=76, discipline=8, lecturer=24, group=7, combined_code=8, **course_params),
    Course(id=77, discipline=8, lecturer=25, group=7, combined_code=None, **course_params),
    Course(id=78, discipline=9, lecturer=27, group=7, combined_code=9, **course_params),
    Course(id=79, discipline=9, lecturer=28, group=7, combined_code=None, **course_params),

    # Группа 8
    Course(id=80, discipline=5, lecturer=15, group=8, combined_code=5, **course_params),
    Course(id=81, discipline=5, lecturer=17, group=8, combined_code=None, **course_params),
    Course(id=82, discipline=6, lecturer=18, group=8, combined_code=6, **course_params),
    Course(id=83, discipline=6, lecturer=20, group=8, combined_code=None, **course_params),
    Course(id=84, discipline=7, lecturer=21, group=8, combined_code=7, **course_params),
    Course(id=85, discipline=7, lecturer=23, group=8, combined_code=None, **course_params),
    Course(id=86, discipline=8, lecturer=24, group=8, combined_code=8, **course_params),
    Course(id=87, discipline=8, lecturer=26, group=8, combined_code=None, **course_params),
    Course(id=88, discipline=9, lecturer=27, group=8, combined_code=9, **course_params),
    Course(id=89, discipline=9, lecturer=29, group=8, combined_code=None, **course_params),

    # Группа 9
    Course(id=90, discipline=5, lecturer=15, group=9, combined_code=5, **course_params),
    Course(id=91, discipline=5, lecturer=17, group=9, combined_code=None, **course_params),
    Course(id=92, discipline=6, lecturer=18, group=9, combined_code=6, **course_params),
    Course(id=93, discipline=6, lecturer=20, group=9, combined_code=None, **course_params),
    Course(id=94, discipline=7, lecturer=21, group=9, combined_code=7, **course_params),
    Course(id=95, discipline=7, lecturer=23, group=9, combined_code=None, **course_params),
    Course(id=96, discipline=8, lecturer=24, group=9, combined_code=8, **course_params),
    Course(id=97, discipline=8, lecturer=26, group=9, combined_code=None, **course_params),
    Course(id=98, discipline=9, lecturer=27, group=9, combined_code=9, **course_params),
    Course(id=99, discipline=9, lecturer=29, group=9, combined_code=None, **course_params),


    # Группа 10
    Course(id=100, discipline=10, lecturer=30, group=10, combined_code=10, **course_params),
    Course(id=101, discipline=10, lecturer=30, group=10, combined_code=None, **course_params),
    Course(id=102, discipline=11, lecturer=33, group=10, combined_code=11, **course_params),
    Course(id=103, discipline=11, lecturer=33, group=10, combined_code=None, **course_params),
    Course(id=104, discipline=12, lecturer=36, group=10, combined_code=12, **course_params),
    Course(id=105, discipline=12, lecturer=36, group=10, combined_code=None, **course_params),
    Course(id=106, discipline=13, lecturer=39, group=10, combined_code=13, **course_params),
    Course(id=107, discipline=13, lecturer=39, group=10, combined_code=None, **course_params),
    Course(id=108, discipline=14, lecturer=42, group=10, combined_code=14, **course_params),
    Course(id=109, discipline=14, lecturer=42, group=10, combined_code=None, **course_params),

    # Группа 11
    Course(id=110, discipline=10, lecturer=30, group=11, combined_code=10, **course_params),
    Course(id=111, discipline=10, lecturer=31, group=11, combined_code=None, **course_params),
    Course(id=112, discipline=11, lecturer=33, group=11, combined_code=11, **course_params),
    Course(id=113, discipline=11, lecturer=34, group=11, combined_code=None, **course_params),
    Course(id=114, discipline=12, lecturer=36, group=11, combined_code=12, **course_params),
    Course(id=115, discipline=12, lecturer=37, group=11, combined_code=None, **course_params),
    Course(id=116, discipline=13, lecturer=39, group=11, combined_code=13, **course_params),
    Course(id=117, discipline=13, lecturer=40, group=11, combined_code=None, **course_params),
    Course(id=118, discipline=14, lecturer=42, group=11, combined_code=14, **course_params),
    Course(id=119, discipline=14, lecturer=43, group=11, combined_code=None, **course_params),

    # Группа 12
    Course(id=120, discipline=10, lecturer=30, group=12, combined_code=10, **course_params),
    Course(id=121, discipline=10, lecturer=31, group=12, combined_code=None, **course_params),
    Course(id=122, discipline=11, lecturer=33, group=12, combined_code=11, **course_params),
    Course(id=123, discipline=11, lecturer=34, group=12, combined_code=None, **course_params),
    Course(id=124, discipline=12, lecturer=36, group=12, combined_code=12, **course_params),
    Course(id=125, discipline=12, lecturer=37, group=12, combined_code=None, **course_params),
    Course(id=126, discipline=13, lecturer=39, group=12, combined_code=13, **course_params),
    Course(id=127, discipline=13, lecturer=40, group=12, combined_code=None, **course_params),
    Course(id=128, discipline=14, lecturer=42, group=12, combined_code=14, **course_params),
    Course(id=129, discipline=14, lecturer=43, group=12, combined_code=None, **course_params),

    # Группа 13
    Course(id=130, discipline=10, lecturer=30, group=13, combined_code=10, **course_params),
    Course(id=131, discipline=10, lecturer=32, group=13, combined_code=None, **course_params),
    Course(id=132, discipline=11, lecturer=33, group=13, combined_code=11, **course_params),
    Course(id=133, discipline=11, lecturer=35, group=13, combined_code=None, **course_params),
    Course(id=134, discipline=12, lecturer=36, group=13, combined_code=12, **course_params),
    Course(id=135, discipline=12, lecturer=38, group=13, combined_code=None, **course_params),
    Course(id=136, discipline=13, lecturer=39, group=13, combined_code=13, **course_params),
    Course(id=137, discipline=13, lecturer=41, group=13, combined_code=None, **course_params),
    Course(id=138, discipline=14, lecturer=42, group=13, combined_code=14, **course_params),
    Course(id=139, discipline=14, lecturer=44, group=13, combined_code=None, **course_params),

    # Группа 14
    Course(id=140, discipline=10, lecturer=30, group=14, combined_code=10, **course_params),
    Course(id=141, discipline=10, lecturer=12, group=14, combined_code=None, **course_params),
    Course(id=142, discipline=11, lecturer=33, group=14, combined_code=11, **course_params),
    Course(id=143, discipline=11, lecturer=25, group=14, combined_code=None, **course_params),
    Course(id=144, discipline=12, lecturer=36, group=14, combined_code=12, **course_params),
    Course(id=145, discipline=12, lecturer=28, group=14, combined_code=None, **course_params),
    Course(id=146, discipline=13, lecturer=39, group=14, combined_code=13, **course_params),
    Course(id=147, discipline=13, lecturer=41, group=14, combined_code=None, **course_params),
    Course(id=148, discipline=14, lecturer=42, group=14, combined_code=14, **course_params),
    Course(id=149, discipline=14, lecturer=44, group=14, combined_code=None, **course_params),


    # Группа 15
    Course(id=150, discipline=15, lecturer=45, group=15, combined_code=15, **course_params),
    Course(id=151, discipline=15, lecturer=45, group=15, combined_code=None, **course_params),
    Course(id=152, discipline=16, lecturer=48, group=15, combined_code=16, **course_params),
    Course(id=153, discipline=16, lecturer=48, group=15, combined_code=None, **course_params),
    Course(id=154, discipline=17, lecturer=51, group=15, combined_code=17, **course_params),
    Course(id=155, discipline=17, lecturer=51, group=15, combined_code=None, **course_params),
    Course(id=156, discipline=18, lecturer=54, group=15, combined_code=18, **course_params),
    Course(id=157, discipline=18, lecturer=54, group=15, combined_code=None, **course_params),
    Course(id=158, discipline=19, lecturer=57, group=15, combined_code=19, **course_params),
    Course(id=159, discipline=19, lecturer=57, group=15, combined_code=None, **course_params),

    # Группа 16
    Course(id=160, discipline=15, lecturer=45, group=16, combined_code=15, **course_params),
    Course(id=161, discipline=15, lecturer=46, group=16, combined_code=None, **course_params),
    Course(id=162, discipline=16, lecturer=48, group=16, combined_code=16, **course_params),
    Course(id=163, discipline=16, lecturer=49, group=16, combined_code=None, **course_params),
    Course(id=164, discipline=17, lecturer=51, group=16, combined_code=17, **course_params),
    Course(id=165, discipline=17, lecturer=52, group=16, combined_code=None, **course_params),
    Course(id=166, discipline=18, lecturer=54, group=16, combined_code=18, **course_params),
    Course(id=167, discipline=18, lecturer=55, group=16, combined_code=None, **course_params),
    Course(id=168, discipline=19, lecturer=57, group=16, combined_code=19, **course_params),
    Course(id=169, discipline=19, lecturer=58, group=16, combined_code=None, **course_params),

    # Группа 17
    Course(id=170, discipline=15, lecturer=45, group=17, combined_code=15, **course_params),
    Course(id=171, discipline=15, lecturer=46, group=17, combined_code=None, **course_params),
    Course(id=172, discipline=16, lecturer=48, group=17, combined_code=16, **course_params),
    Course(id=173, discipline=16, lecturer=49, group=17, combined_code=None, **course_params),
    Course(id=174, discipline=17, lecturer=51, group=17, combined_code=17, **course_params),
    Course(id=175, discipline=17, lecturer=52, group=17, combined_code=None, **course_params),
    Course(id=176, discipline=18, lecturer=54, group=17, combined_code=18, **course_params),
    Course(id=177, discipline=18, lecturer=55, group=17, combined_code=None, **course_params),
    Course(id=178, discipline=19, lecturer=57, group=17, combined_code=19, **course_params),
    Course(id=179, discipline=19, lecturer=58, group=17, combined_code=None, **course_params),

    # Группа 18
    Course(id=180, discipline=15, lecturer=45, group=18, combined_code=15, **course_params),
    Course(id=181, discipline=15, lecturer=47, group=18, combined_code=None, **course_params),
    Course(id=182, discipline=16, lecturer=48, group=18, combined_code=16, **course_params),
    Course(id=183, discipline=16, lecturer=50, group=18, combined_code=None, **course_params),
    Course(id=184, discipline=17, lecturer=51, group=18, combined_code=17, **course_params),
    Course(id=185, discipline=17, lecturer=53, group=18, combined_code=None, **course_params),
    Course(id=186, discipline=18, lecturer=54, group=18, combined_code=18, **course_params),
    Course(id=187, discipline=18, lecturer=56, group=18, combined_code=None, **course_params),
    Course(id=188, discipline=19, lecturer=57, group=18, combined_code=19, **course_params),
    Course(id=189, discipline=19, lecturer=59, group=18, combined_code=None, **course_params),

    # Группа 19
    Course(id=190, discipline=15, lecturer=45, group=19, combined_code=15, **course_params),
    Course(id=191, discipline=15, lecturer=47, group=19, combined_code=None, **course_params),
    Course(id=192, discipline=16, lecturer=48, group=19, combined_code=16, **course_params),
    Course(id=193, discipline=16, lecturer=50, group=19, combined_code=None, **course_params),
    Course(id=194, discipline=17, lecturer=51, group=19, combined_code=17, **course_params),
    Course(id=195, discipline=17, lecturer=53, group=19, combined_code=None, **course_params),
    Course(id=196, discipline=18, lecturer=54, group=19, combined_code=18, **course_params),
    Course(id=197, discipline=18, lecturer=56, group=19, combined_code=None, **course_params),
    Course(id=198, discipline=19, lecturer=57, group=19, combined_code=19, **course_params),
    Course(id=199, discipline=19, lecturer=59, group=19, combined_code=None, **course_params),
]

classrooms = [
    Classroom(id=0, capacity=30),
    Classroom(id=1, capacity=30),
    Classroom(id=2, capacity=30),
    Classroom(id=3, capacity=30),
    Classroom(id=4, capacity=30),
    Classroom(id=5, capacity=30),
    Classroom(id=6, capacity=30),
    Classroom(id=7, capacity=30),
    Classroom(id=8, capacity=180),
    Classroom(id=9, capacity=180),
    Classroom(id=10, capacity=180),
    Classroom(id=11, capacity=180),
]

timeslots = [
    Timeslot(
        id=w * DPW * CPD + d * CPD + c,
        week=w,
        day=d,
        class_number=c
    )
    for w in range(14) for d in range(DPW) for c in range(CPD)
]

classroom_equipment = []

required_equipment = []
