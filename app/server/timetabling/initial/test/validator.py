import copy

from app.server.timetabling.models.timeslot import CPD, DPW


class Validator:

    @staticmethod
    def validate(courses, classrooms, timeslots, classroom_equipment, required_equipment, alpha, tau, log=False):
        timeslots = sorted(timeslots, key=lambda item: int(item))

        time_template = [[[[] for cls in range(CPD)] for day in range(DPW)] for week in range(timeslots[-1].week + 1)]

        lecturers = set([course.lecturer for course in courses])
        groups = set([course.group for course in courses])

        group_map = {group: copy.deepcopy(time_template) for group in groups}
        classroom_map = {classroom.id: copy.deepcopy(time_template) for classroom in classrooms}
        lecturer_map = {lecturer: copy.deepcopy(time_template) for lecturer in lecturers}
        classroom_capacity_map = {classroom.id: copy.deepcopy(time_template) for classroom in classrooms}

        for course, assigned_classroom_id, assigned_timeslot_id in zip(courses, alpha, tau):
            classroom = next(classroom for classroom in classrooms if classroom.id == assigned_classroom_id)
            initial_timeslot = next(timeslot for timeslot in timeslots if timeslot.id == assigned_timeslot_id)
            for week_shift in range(course.duration):
                for block_shift in range(course.block_length):
                    week = initial_timeslot.week + week_shift
                    day = initial_timeslot.day
                    cls = initial_timeslot.class_number + block_shift

                    group_map[course.group][week][day][cls].append(course)
                    lecturer_map[course.lecturer][week][day][cls].append(course)
                    classroom_map[classroom.id][week][day][cls].append(course)
                    classroom_capacity_map[classroom.id][week][day][cls].append(course.group_size)

        group_violations = set()
        for group_id, course_map in group_map.items():
            for week in course_map:
                for day in week:
                    for cls in day:
                        if len(cls) > 1:
                            if len(cls) == 2 and cls[0].partition + cls[1].partition <= 1:
                                break
                            group_violations.update([course.id for course in cls])

        lecturer_violations = set()
        for lecturer_id, course_map in lecturer_map.items():
            for week in course_map:
                for day in week:
                    for cls in day:
                        combined_codes = set([course.combined_code for course in cls])
                        if None in combined_codes:
                            combined_codes.remove(None)
                        if len(cls) > 1 and len(combined_codes) != 1:
                            lecturer_violations.update([course.id for course in cls])

        classroom_violations = set()
        for classroom_id, course_map in classroom_map.items():
            for week in course_map:
                for day in week:
                    for cls in day:
                        combined_codes = set([course.combined_code for course in cls])
                        if None in combined_codes:
                            combined_codes.remove(None)
                        if len(cls) > 1 and len(combined_codes) != 1:
                            classroom_violations.update([course.id for course in cls])

        valid_classroom_violations = set()
        for i, course in enumerate(courses):
            if course.valid_classrooms is not None and alpha[i] not in course.valid_classrooms:
                valid_classroom_violations.add(course.id)

        classroom_capacity_violation = set()
        for classroom_id, course_map in classroom_map.items():
            for week in course_map:
                for day in week:
                    for cls in day:
                        classroom = next(classroom for classroom in classrooms if classroom.id == classroom_id)
                        if classroom.capacity < sum([course.group_size for course in cls]):
                            classroom_capacity_violation.update([course.id for course in cls])

        classroom_equipment_violation = set()
        for assigned_classroom_id, course in zip(alpha, courses):
            required_equipment = [eq for eq in required_equipment if eq.course == course.id]
            classroom_equipment = [eq for eq in classroom_equipment if eq.classroom == assigned_classroom_id]

            for r_eq in required_equipment:
                present = False
                for c_eq in classroom_equipment:
                    if r_eq.equipment_type == c_eq.equipment_type and r_eq.amount <= c_eq.amount:
                        present = True
                        break
                if not present:
                    classroom_equipment_violation.add(course.id)

        time_interval_violation = set()
        for i, course in enumerate(courses):
            if course.timeslot_from is not None:
                timeslot_from = next(timeslot for timeslot in timeslots if timeslot.id == course.timeslot_from)
                actual_timeslot_from = next(timeslot for timeslot in timeslots if timeslot.id == tau[i])
                if int(actual_timeslot_from) < int(timeslot_from):
                    time_interval_violation.add(course.id)
            if course.timeslot_to is not None:
                timeslot_to = next(timeslot for timeslot in timeslots if timeslot.id == course.timeslot_to)
                actual_timeslot_from = next(timeslot for timeslot in timeslots if timeslot.id == tau[i])
                actual_timeslot_to = copy.deepcopy(actual_timeslot_from)
                actual_timeslot_to.week += (course.duration - 1) * course.week_intensity
                if int(actual_timeslot_to) > int(timeslot_to):
                    time_interval_violation.add(course.id)

        course_chain_violation = set()
        chained_courses = {}
        for i, course in enumerate(courses):
            if course.chain_code is not None:
                if course.chain_code in chained_courses:
                    chained_courses[course.chain_code].append((i, course))
                else:
                    chained_courses[course.chain_code] = [(i, course)]

        for chain_code, courses in chained_courses.items():
            for i, course_i in courses:
                chained = True
                for j, course_j in courses:
                    if course_i.chain_priority > course_j.chain_priority and tau[i] <= tau[j]:
                        chained = False
                        break
                    elif course_i.chain_priority < course_j.chain_priority and tau[i] >= tau[j]:
                        chained = False
                        break
                if not chained:
                    course_chain_violation.add(course_i.id)

        if log:
            print(f'Alpha: {alpha}')
            print(f'Tau: {tau}')
            print('\n___________________________\n')
            print(f'Groups violation: {group_violations}')
            print(f'Classroom violation: {classroom_violations}')
            print(f'Lecturer violation: {lecturer_violations}')
            print(f'Valid classroom violation: {valid_classroom_violations}')
            print(f'Classroom capacity violation: {classroom_capacity_violation}')
            print(f'Classroom equipment violation: {classroom_equipment_violation}')
            print(f'Time interval violation: {time_interval_violation}')
            print(f'Course chain violation: {course_chain_violation}')

        return sum(list(map(len, [
            group_violations,
            classroom_violations,
            lecturer_violations,
            valid_classroom_violations,
            classroom_capacity_violation,
            classroom_equipment_violation,
            time_interval_violation,
            course_chain_violation
        ]))) == 0
