import asyncio

from sqlalchemy import text

from app.server.database.database import async_session_maker
from app.server.database.models import Institution, Classroom, Department, Item, \
    Project, EducationProgram, ClassroomEquipment, Lecturer


async def clear_db(force=False):
    async with async_session_maker() as session:

        if force:
            await session.execute(text('TRUNCATE TABLE "user" RESTART IDENTITY CASCADE'))

        await session.execute(text('TRUNCATE TABLE "chain" RESTART IDENTITY CASCADE'))
        await session.execute(text('TRUNCATE TABLE "classroom" RESTART IDENTITY CASCADE'))
        await session.execute(text('TRUNCATE TABLE "classroom_equipment" RESTART IDENTITY CASCADE'))
        await session.execute(text('TRUNCATE TABLE "classroom_pool" RESTART IDENTITY CASCADE'))
        await session.execute(text('TRUNCATE TABLE "classroom_pool_classroom" RESTART IDENTITY CASCADE'))
        await session.execute(text('TRUNCATE TABLE "classroom_time_slot" RESTART IDENTITY CASCADE'))
        await session.execute(text('TRUNCATE TABLE "combination" RESTART IDENTITY CASCADE'))
        await session.execute(text('TRUNCATE TABLE "course" RESTART IDENTITY CASCADE'))
        await session.execute(text('TRUNCATE TABLE "department" RESTART IDENTITY CASCADE'))
        await session.execute(text('TRUNCATE TABLE "discipline" RESTART IDENTITY CASCADE'))
        await session.execute(text('TRUNCATE TABLE "education_block" RESTART IDENTITY CASCADE'))
        await session.execute(text('TRUNCATE TABLE "education_module" RESTART IDENTITY CASCADE'))
        await session.execute(text('TRUNCATE TABLE "education_program" RESTART IDENTITY CASCADE'))
        await session.execute(text('TRUNCATE TABLE "group" RESTART IDENTITY CASCADE'))
        await session.execute(text('TRUNCATE TABLE "institution" RESTART IDENTITY CASCADE'))
        await session.execute(text('TRUNCATE TABLE "item" RESTART IDENTITY CASCADE'))
        await session.execute(text('TRUNCATE TABLE "lecturer" RESTART IDENTITY CASCADE'))
        await session.execute(text('TRUNCATE TABLE "preference" RESTART IDENTITY CASCADE'))
        await session.execute(text('TRUNCATE TABLE "project" RESTART IDENTITY CASCADE'))
        await session.execute(text('TRUNCATE TABLE "required_equipment" RESTART IDENTITY CASCADE'))
        await session.execute(text('TRUNCATE TABLE "time_slot" RESTART IDENTITY CASCADE'))


        await session.commit()


async def generate_projects():
    async with async_session_maker() as session:
        session.add(Project(user=1, name='Осенний семестр'))
        session.add(Project(user=1, name='Весенний семестр'))

        await session.commit()




async def generate_items():
    async with async_session_maker() as session:
        session.add(Item(user=1, name='Микрофон'))
        session.add(Item(user=1, name='Проектор'))
        session.add(Item(user=1, name='Компьютер'))
        session.add(Item(user=1, name='Меловая доска'))
        session.add(Item(user=1, name='Маркерная доска'))
        session.add(Item(user=1, name='Электронная доска'))

        await session.commit()


async def generate_classrooms():
    async with async_session_maker() as session:

        # ----------------------------- ГЗ  -----------------------------

        session.add(Classroom(user=1, building='ГЗ', auditory_number='237', capacity=250))
        session.add(ClassroomEquipment(user=1, classroom=1, item=1, amount=2))
        session.add(ClassroomEquipment(user=1, classroom=1, item=2, amount=1))
        session.add(ClassroomEquipment(user=1, classroom=1, item=5, amount=2))

        # -------------------------- 9 КОРПУС  --------------------------

        # Схемотехника операционных устройств и ОВТ
        session.add(Classroom(user=1, building='9', auditory_number='204', capacity=24))
        session.add(Classroom(user=1, building='9', auditory_number='216', capacity=24))

        # МПС и Архитектура ЭВМ
        session.add(Classroom(user=1, building='9', auditory_number='211', capacity=24))
        session.add(Classroom(user=1, building='9', auditory_number='213', capacity=24))

        # Интерфейсы внешних устройств
        session.add(Classroom(user=1, building='9', auditory_number='313', capacity=24))

        # -------------------------- 3 КОРПУС  --------------------------

        # Компьютерная графика (Бакалавриат), Встраиваемые системы (Магистратура)
        session.add(Classroom(user=1, building='3', auditory_number='302', capacity=24))

        # Общая аудитория для практики без оборудования
        session.add(Classroom(user=1, building='3', auditory_number='303', capacity=24))

        # МПС, Архитектура ЭВМ
        session.add(Classroom(user=1, building='3', auditory_number='400', capacity=24))

        # Лекционная аудитория
        session.add(Classroom(user=1, building='3', auditory_number='401', capacity=80))
        session.add(ClassroomEquipment(user=1, classroom=1, item=1, amount=1))
        session.add(ClassroomEquipment(user=1, classroom=1, item=2, amount=1))
        session.add(ClassroomEquipment(user=1, classroom=1, item=5, amount=2))

        # Компьютерный класс общего пользования
        session.add(Classroom(user=1, building='3', auditory_number='402', capacity=24))
        session.add(Classroom(user=1, building='3', auditory_number='404', capacity=24))
        session.add(Classroom(user=1, building='3', auditory_number='404a', capacity=24))

        # Лаб. Антонова (Магистры) - АПДУ, Средства проекитрования аппаратуры ЦОС,
        # Технологии проектирования аппаратных средств комп. систем
        # Проектирование реконфигурируемых гибридных выч. систем
        session.add(Classroom(user=1, building='3', auditory_number='408', capacity=15))

        # Лаб. Антонова (Бакалавры) - Языки описания и АПДУ
        session.add(Classroom(user=1, building='3', auditory_number='410', capacity=24))

        # Операционные системы
        session.add(Classroom(user=1, building='3', auditory_number='405', capacity=15))

        # ------------------------- 11 КОРПУС  --------------------------

        # Лекционные
        session.add(Classroom(user=1, building='11', auditory_number='319', capacity=90))
        session.add(Classroom(user=1, building='11', auditory_number='148', capacity=110))
        session.add(Classroom(user=1, building='11', auditory_number='143', capacity=110))

        # Практические (без компов)
        session.add(Classroom(user=1, building='11', auditory_number='309', capacity=50))
        session.add(Classroom(user=1, building='11', auditory_number='315', capacity=40))
        session.add(Classroom(user=1, building='11', auditory_number='316', capacity=40))
        session.add(Classroom(user=1, building='11', auditory_number='321', capacity=40))
        session.add(Classroom(user=1, building='11', auditory_number='323', capacity=40))
        session.add(Classroom(user=1, building='11', auditory_number='324', capacity=40))
        session.add(Classroom(user=1, building='11', auditory_number='326', capacity=40))
        session.add(Classroom(user=1, building='11', auditory_number='328', capacity=40))
        session.add(Classroom(user=1, building='11', auditory_number='330', capacity=40))
        session.add(Classroom(user=1, building='11', auditory_number='322', capacity=26))
        session.add(Classroom(user=1, building='11', auditory_number='332', capacity=20))

        await session.commit()



async def generate_institutions():
    async with async_session_maker() as session:

        session.add(Institution(user=1, code=38, name='Гуманитарный институт'))
        session.add(Institution(user=1, code=31, name='Инженерно-строительный институт'))
        session.add(Institution(user=1, code=47, name='Институт биомедицинских систем и биотехнологий'))
        session.add(Institution(user=1, code=48, name='Институт кибербезопасности и защиты информации'))
        session.add(Institution(user=1, code=35, name='Институт компьютерных наук и технологий'))
        session.add(Institution(user=1, code=33, name='Институт машиностроения, материалов и транспорта'))
        session.add(Institution(user=1, code=43, name='Институт передовых производственных технологий'))
        session.add(Institution(user=1, code=42, name='Институт физической культуры, спорта и туризма'))
        session.add(Institution(user=1, code=49, name='Институт электроники и телекоммуникаций'))
        session.add(Institution(user=1, code=32, name='Институт энергетики'))
        session.add(Institution(user=1, code=50, name='Физико-мехнический институт'))
        session.add(Institution(user=1, code=37, name='Институт промышленного менеджмента, экономики и торговли'))

        await session.commit()


async def generate_education_programs():
    async with async_session_maker() as session:

        # ---------------------- ИВТ БАКАЛАВРИАТ  -----------------------

        session.add(
            EducationProgram(
                user=1, code='09.03.01', name='Информатика и вычислительная техника',
                profile_code='01', profile_name='Разработка компьютерных систем',
                education_level=EducationProgram.EducationLevel.BACHELOR
            )
        )

        session.add(
            EducationProgram(
                user=1, code='09.03.01', name='Информатика и вычислительная техника',
                profile_code='02', profile_name='Технологии разработки программного обеспечения',
                education_level=EducationProgram.EducationLevel.BACHELOR
            )
        )

        # ---------------------- ИВТ МАГИСТРАТУРА  ----------------------

        session.add(
            EducationProgram(
                user=1, code='09.04.01', name='Информатика и вычислительная техника',
                profile_code='15',
                profile_name='Технологии проектирования системного и прикладного программного обеспечения',
                education_level=EducationProgram.EducationLevel.MASTER
            )
        )

        session.add(
            EducationProgram(
                user=1, code='09.04.01', name='Информатика и вычислительная техника',
                profile_code='20',
                profile_name='Проектирование интеллектуальных компьютерных систем',
                education_level=EducationProgram.EducationLevel.MASTER
            )
        )

        # ---------------------- ИВТ АСПИРАНТУРА  -----------------------

        session.add(
            EducationProgram(
                user=1, code='09.06.01', name='Информатика и вычислительная техника',
                profile_code='03',
                profile_name='Элементы и устройства вычислительной техники и систем управления',
                education_level=EducationProgram.EducationLevel.POSTGRADUATE
            )
        )

        session.add(
            EducationProgram(
                user=1, code='09.06.01', name='Информатика и вычислительная техника',
                profile_code='10',
                profile_name='Теоретические основы информатики',
                education_level=EducationProgram.EducationLevel.POSTGRADUATE
            )
        )

        # ----------------------- ПИ БАКАЛАВРИАТ  -----------------------

        session.add(
            EducationProgram(
                user=1, code='09.03.03', name='Прикладная информатика',
                profile_code='03',
                profile_name='Интеллектуальные инфокоммуникационные технологии',
                education_level=EducationProgram.EducationLevel.BACHELOR
            )
        )

        # ---------------------- ПИ МАГИСТРАТУРА  -----------------------

        session.add(
            EducationProgram(
                user=1, code='09.04.03', name='Прикладная информатика',
                profile_code='04',
                profile_name='Интеллектуальные технологии управления знаниями и данными',
                education_level=EducationProgram.EducationLevel.MASTER
            )
        )

        await session.commit()


async def generate_departments():
    async with async_session_maker() as session:
        session.add(Department(user=1, institution=5, name='Высшая школа киберфизических систем и управления'))
        session.add(Department(user=1, institution=5, name='Высшая школа интеллектуальных систем и суперкомпьютерных технологий'))
        session.add(Department(user=1, institution=5, name='Высшая школа искусственного интеллекта'))
        session.add(Department(user=1, institution=5, name='Высшая школа программной инженерии'))

        await session.commit()

async def generate_lecturers():
    async with async_session_maker() as session:
        session.add(Lecturer(user=1, name='Абдуллин Азат Марселевич', department=2))
        session.add(Lecturer(user=1, name='Абрамова Марина Геннадьевна', department=2))
        session.add(Lecturer(user=1, name='Алексеев Сергей Владимирович', department=2))
        session.add(Lecturer(user=1, name='Алексюк Артем Олегович', department=2))
        session.add(Lecturer(user=1, name='Андрианова Екатерина Евгеньевна', department=2))
        session.add(Lecturer(user=1, name='Афанасьев Илья Михайлович', department=2))
        session.add(Lecturer(user=1, name='Белых Игорь Николаевич', department=2))
        session.add(Lecturer(user=1, name='Брык Иван Юрьевич', department=2))
        session.add(Lecturer(user=1, name='Васильянов Г.С.', department=2))
        session.add(Lecturer(user=1, name='Вербова Наталья Михайловна', department=2))
        session.add(Lecturer(user=1, name='Веремьев Виктор Леонтьевич', department=2))
        session.add(Lecturer(user=1, name='Галкин Александр Сергеевич', department=2))
        session.add(Lecturer(user=1, name='Гринберг Эльвира Яковлевна', department=2))
        session.add(Lecturer(user=1, name='Егорова Инга Сергеевна', department=2))
        session.add(Lecturer(user=1, name='Ерошкин Александр Владимирович', department=2))
        session.add(Lecturer(user=1, name='Зорин Арсений Геннадьевич', department=2))
        session.add(Lecturer(user=1, name='Иванищев Алексей Вячеславович', department=2))
        session.add(Lecturer(user=1, name='Киселев Иван Олегович', department=2))
        session.add(Lecturer(user=1, name='Коваленко Геннадий Васильевич', department=2))
        session.add(Lecturer(user=1, name='Комарова Елена Викторовна', department=2))
        session.add(Lecturer(user=1, name='Кораблев Алексей Владимирович', department=2))
        session.add(Lecturer(user=1, name='Коренев Дмитрий Алексеевич', department=2))
        session.add(Lecturer(user=1, name='Кубельский Мирослав Валерьевич', department=2))
        session.add(Lecturer(user=1, name='Кудрявцев Дмитрий Вячеславович', department=2))
        session.add(Lecturer(user=1, name='Липанова Ирина Александровна', department=2))
        session.add(Lecturer(user=1, name='Михалев Сергей Сергеевич', department=2))
        session.add(Lecturer(user=1, name='Мяснов Александр Владимирович', department=2))
        session.add(Lecturer(user=1, name='Орлов Егор Сергеевич', department=2))
        session.add(Lecturer(user=1, name='Пак Вадим Геннадьевич', department=2))
        session.add(Lecturer(user=1, name='Пархоменко Владимир Андреевич', department=2))
        session.add(Lecturer(user=1, name='Перезябов Олег Аркадьевич', department=2))
        session.add(Lecturer(user=1, name='Плотникова Ксения Евгеньевна', department=2))
        session.add(Lecturer(user=1, name='Ракова Валерия Владимировна', department=2))
        session.add(Lecturer(user=1, name='Резединова Евгения Юрьевна', department=2))
        session.add(Lecturer(user=1, name='Сабинин Олег Юрьевич', department=2))
        session.add(Lecturer(user=1, name='Сергеев Анатолий Васильевич', department=2))
        session.add(Lecturer(user=1, name='Соболь Валентин', department=2))
        session.add(Lecturer(user=1, name='Степанов Даниил Сергеевич', department=2))
        session.add(Lecturer(user=1, name='Тарасов Олег Михайлович', department=2))
        session.add(Lecturer(user=1, name='Туральчук Константин Анатольевич', department=2))
        session.add(Lecturer(user=1, name='Тушканова Ольга Николаевна', department=2))
        session.add(Lecturer(user=1, name='Хахина Анна Михайловна', department=2))
        session.add(Lecturer(user=1, name='Хитров Егор Германович', department=2))
        session.add(Lecturer(user=1, name='Цесько Вадим Александрович', department=2))
        session.add(Lecturer(user=1, name='Черкасова Танзиля Халитовна', department=2))
        session.add(Lecturer(user=1, name='Щукин Александр Валентинович', department=2))

        session.add(Lecturer(user=1, name='Абрамов Николай Александрович', department=2))
        session.add(Lecturer(user=1, name='Антонов Александр Петрович', department=2))
        session.add(Lecturer(user=1, name='Антонов Андрей Андреевич', department=2))
        session.add(Lecturer(user=1, name='Ахин Марат Халимович', department=2))
        session.add(Lecturer(user=1, name='Бабко Леонид Васильевич', department=2))
        session.add(Lecturer(user=1, name='Балтруков Николай Николаевич', department=2))
        session.add(Lecturer(user=1, name='Беляев Михаил Анатольевич', department=2))
        session.add(Lecturer(user=1, name='Бендерская Елена Николаевна', department=2))
        session.add(Lecturer(user=1, name='Богач Наталья Владимировна', department=2))
        session.add(Lecturer(user=1, name='Болсуновская Марина Владимировна', department=2))
        session.add(Lecturer(user=1, name='Васильев Алексей Евгеньевич', department=2))
        session.add(Lecturer(user=1, name='Вылегжанина Карина Дмитриевна', department=2))
        session.add(Lecturer(user=1, name='Гагарский Кирилл Алексеевич', department=2))
        session.add(Lecturer(user=1, name='Глухих Михаил Игоревич', department=2))
        session.add(Lecturer(user=1, name='Гульфи Николя Жульен', department=2))
        session.add(Lecturer(user=1, name='Давыдов Владимир Григорьевич', department=2))
        session.add(Lecturer(user=1, name='Душутина Елена Владимировна', department=2))
        session.add(Lecturer(user=1, name='Ельцов Александр Александрович', department=2))
        session.add(Lecturer(user=1, name='Жвариков Владимир Анатольевич', department=2))
        session.add(Lecturer(user=1, name='Жуков Андрей Владимирович', department=2))
        session.add(Lecturer(user=1, name='Жукова С.В.', department=2))
        session.add(Lecturer(user=1, name='Зозуля Алексей Викторович', department=2))
        session.add(Lecturer(user=1, name='Иванов Олег Иванович', department=2))
        session.add(Lecturer(user=1, name='Ицыксон Владимир Михайлович', department=2))
        session.add(Lecturer(user=1, name='Каррабина Бордоль Хорди', department=2))
        session.add(Lecturer(user=1, name='Кастелльс Руфас Давид', department=2))
        session.add(Lecturer(user=1, name='Королев Вячеслав Семенович', department=2))
        session.add(Lecturer(user=1, name='Кочетков Юрий Дмитриевич', department=2))
        session.add(Lecturer(user=1, name='Кошелев Сергей Иванович', department=2))
        session.add(Lecturer(user=1, name='Кузнецов Андрей Николаевич', department=2))
        session.add(Lecturer(user=1, name='Кузьмин Александр Александрович', department=2))
        session.add(Lecturer(user=1, name='Лавров Алексей Александрович', department=2))
        session.add(Lecturer(user=1, name='Лексашов Александр Викторович', department=2))
        session.add(Lecturer(user=1, name='Леонтьев Александр Георгиевич', department=2))
        session.add(Lecturer(user=1, name='Лупин Анатолий Викторович', department=2))
        session.add(Lecturer(user=1, name='Максименко Сергей Леонидович', department=2))
        session.add(Lecturer(user=1, name='Малышев Игорь Алексеевич', department=2))
        session.add(Lecturer(user=1, name='Мамутова Ольга Вячеславовна', department=2))
        session.add(Lecturer(user=1, name='Мараховский Вячеслав Борисович', department=2))
        session.add(Lecturer(user=1, name='Мелехин Виктор Федорович', department=2))
        session.add(Lecturer(user=1, name='Митина Татьяна Михайловна', department=2))
        session.add(Lecturer(user=1, name='Михайлов Александр Николаевич', department=2))
        session.add(Lecturer(user=1, name='Моисеев Михаил Юрьевич', department=2))
        session.add(Lecturer(user=1, name='Нестеров Сергей  Александрович', department=2))
        session.add(Lecturer(user=1, name='Никитин Кирилл Вячеславович', department=2))
        session.add(Lecturer(user=1, name='Новопашенный Андрей Гелиевич', department=2))
        session.add(Lecturer(user=1, name='Павловский Евгений Григорьевич', department=2))
        session.add(Lecturer(user=1, name='Петров Максим Алексеевич', department=2))
        session.add(Lecturer(user=1, name='Пышкин Евгений Валерьевич', department=2))
        session.add(Lecturer(user=1, name='Сабонис Сергей Станиславович', department=2))
        session.add(Lecturer(user=1, name='Садин Ярослав Дмитриевич', department=2))
        session.add(Lecturer(user=1, name='Сиднев Александр Георгиевич', department=2))
        session.add(Lecturer(user=1, name='Сидорина Татьяна Леонидовна', department=2))
        session.add(Lecturer(user=1, name='Скобцов Юрий Александрович', department=2))
        session.add(Lecturer(user=1, name='Скорубский Владимир Иванович', department=2))
        session.add(Lecturer(user=1, name='Соколова Наталия Викторовна', department=2))
        session.add(Lecturer(user=1, name='Стручков Игорь Вячеславович', department=2))
        session.add(Lecturer(user=1, name='Туркин Евгений Александрович', department=2))
        session.add(Lecturer(user=1, name='Федотов Александр Александрович', department=2))
        session.add(Lecturer(user=1, name='Филиппов Алексей Семенович', department=2))
        session.add(Lecturer(user=1, name='Цыган Владимир Николаевич', department=2))
        session.add(Lecturer(user=1, name='Шейнин Юрий Евгеньевич', department=2))
        session.add(Lecturer(user=1, name='Ярмийчук Владимир Дмитриевич', department=2))

        session.add(Lecturer(user=1, name='Баранов Виктор Ефимович', department=2))
        session.add(Lecturer(user=1, name='Богданов Сергей Сергеевич', department=2))
        session.add(Lecturer(user=1, name='Васильев Андрей Юрьевич', department=2))
        session.add(Lecturer(user=1, name='Волкова Виолетта Николаевна', department=2))
        session.add(Lecturer(user=1, name='Громов Виктор Никифорович', department=2))
        session.add(Lecturer(user=1, name='Ефремов Артем Александрович', department=2))
        session.add(Lecturer(user=1, name='Кимков Валерий Николаевич', department=2))
        session.add(Lecturer(user=1, name='Кирсяев Анатолий Николаевич', department=2))
        session.add(Lecturer(user=1, name='Кисоржевский Владимир Францевич', department=2))
        session.add(Lecturer(user=1, name='Козлов Владимир Николаевич', department=2))
        session.add(Lecturer(user=1, name='Куприянов Валентин Евстафьевич', department=2))
        session.add(Lecturer(user=1, name='Лыпарь Юрий Иванович', department=2))
        session.add(Lecturer(user=1, name='Магер Владимир Евстафьевич', department=2))
        session.add(Lecturer(user=1, name='Манаев Илья Евгеньевич', department=2))
        session.add(Lecturer(user=1, name='Нестеров Сергей Александрович', department=2))
        session.add(Lecturer(user=1, name='Пономарев Алексей Геннадьевич', department=2))
        session.add(Lecturer(user=1, name='Симаков Игорь Павлович', department=2))
        session.add(Lecturer(user=1, name='Станкевич Лев Александрович', department=2))
        session.add(Lecturer(user=1, name='Тросько Игорь Усяславович', department=2))
        session.add(Lecturer(user=1, name='Фирсов Андрей Николаевич', department=2))
        session.add(Lecturer(user=1, name='Хлопин Сергей Владимирович', department=2))
        session.add(Lecturer(user=1, name='Холодных Павел Владимирович', department=2))
        session.add(Lecturer(user=1, name='Черненькая Людмила Васильевна', department=2))
        session.add(Lecturer(user=1, name='Шашихин Владимир Николаевич', department=2))

        await session.commit()


async def generate():
    await clear_db()

    await generate_projects()
    # CLASSROOM POOLS
    await generate_items()
    await generate_classrooms()
    await generate_institutions()
    # COMBINATIONS
    # CHAINS
    # COURSE POOLS

    await generate_education_programs()
    # CLASSROOM POOL CLASSROOM

    await generate_departments()

    await generate_lecturers()



if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(generate())