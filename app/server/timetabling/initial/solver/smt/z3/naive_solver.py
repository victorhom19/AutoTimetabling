import z3
from z3 import Int, SolverFor, Or, Sum, If, And, Implies

from app.server.timetabling.models.timeslot import CPD, DPW
from app.server.timetabling.base_solver import InitialBaseSolver


class Z3NaiveSolver(InitialBaseSolver):

    def __init__(self, courses, classrooms, timeslots, classroom_equipment, required_equipment):
        super().__init__(courses, classrooms, timeslots, classroom_equipment, required_equipment)

        self.solver = SolverFor('QF_LRA')

        self.alpha = [Int(f'alpha_{i}') for i, _ in enumerate(self.courses)]
        self.tau = [Int(f'tau_{i}') for i, _ in enumerate(self.courses)]

        self.tau_week_start = []
        self.tau_week_end = []
        self.tau_week_shift = []

        self.tau_day = []
        self.tau_class_start = []
        self.tau_class_end = []

        for i, course in enumerate(self.courses):
            tau_ws = Int(f'tau_week_start_{i}')
            self.solver.add(tau_ws == self.tau[i] / (DPW * CPD))
            self.tau_week_start.append(tau_ws)

            tau_we = Int(f'tau_week_end_{i}')
            self.solver.add(tau_we == tau_ws + (course.duration - 1) * course.week_intensity)
            self.tau_week_end.append(tau_we)

            tau_wsh = Int(f'tau_week_shift_{i}')
            self.solver.add(tau_wsh == tau_ws % course.week_intensity)
            self.tau_week_shift.append(tau_wsh)

            tau_d = Int(f'tau_day_{i}')
            self.solver.add(tau_d == self.tau[i] / CPD % DPW)
            self.tau_day.append(tau_d)

            tau_cs = Int(f'tau_class_start_{i}')
            self.solver.add(tau_cs == self.tau[i] % CPD)
            self.tau_class_start.append(tau_cs)

            tau_ce = Int(f'tau_class_end_{i}')
            self.solver.add(tau_ce == tau_cs + course.block_length - 1)
            self.tau_class_end.append(tau_ce)


    def init_constraints(self):

        # Alpha space constraint
        for alpha_el in self.alpha:
            constraint_list = []
            for classroom in self.classrooms:
                constraint_list.append(alpha_el == classroom.id)
            self.solver.add(Or(*constraint_list))

        # Tau space constraint
        for tau_el in self.tau:
            constraint_list = []
            for timeslot in self.timeslots:
                constraint_list.append(tau_el == timeslot.id)
            self.solver.add(Or(*constraint_list))

        # Course completeness constraint
        for i, course in enumerate(self.courses):
            self.solver.add(
                And(
                    self.tau_week_end[i] <= self.timeslots[-1].week,
                    self.tau_day[i] <= self.timeslots[-1].day,
                    self.tau_class_end[i] <= self.timeslots[-1].class_number
                ))

        # Block course constraint
        for i, course in enumerate(self.courses):
            if course.block_length > 1:
                self.solver.add(
                    self.tau_class_end[i] <= CPD
                )

        # Combined course constraint
        for i, course_i in enumerate(self.courses):
            for j, course_j in enumerate(self.courses):
                if i < j and course_i.combined_code is not None and course_i.combined_code == course_j.combined_code:
                    self.solver.add(self.alpha[i] == self.alpha[j])
                    self.solver.add(self.tau[i] == self.tau[j])

        # Group overlaying constraint
        for group in self.groups:
            for timeslot in self.timeslots:
                self.solver.add(Sum([
                    If(
                        And(
                            self.tau_week_start[i] <= timeslot.week,
                            timeslot.week <= self.tau_week_end[i],
                            self.tau_week_shift[i] == timeslot.week % course.week_intensity,
                            self.tau_day[i] == timeslot.day,
                            self.tau_class_start[i] <= timeslot.class_number,
                            timeslot.class_number <= self.tau_class_end[i]
                        ),
                        course.partition,
                        0
                    )
                    for i, course in enumerate(self.courses) if course.group == group
                ]) <= 1)

        # Classroom overlaying constraint
        seen_combined = set()
        filter_vec = []
        for course in self.courses:
            if course.combined_code is None:
                filter_vec.append(True)
            elif course.combined_code not in seen_combined:
                filter_vec.append(True)
                seen_combined.add(course.combined_code)
            else:
                filter_vec.append(False)

        for classroom in self.classrooms:
            for timeslot in self.timeslots:
                self.solver.add(Sum([
                    If(
                        And(
                            self.alpha[i] == classroom.id,

                            self.tau_week_start[i] <= timeslot.week,
                            timeslot.week <= self.tau_week_end[i],
                            self.tau_week_shift[i] == timeslot.week % course.week_intensity,
                            self.tau_day[i] == timeslot.day,
                            self.tau_class_start[i] <= timeslot.class_number,
                            timeslot.class_number <= self.tau_class_end[i]
                        ),
                        1,
                        0
                    )
                    for i, course in enumerate(self.courses) if filter_vec[i]
                ]) <= 1)

        # Lecturer overlaying constraint
        for lecturer in self.lecturers:
            for timeslot in self.timeslots:
                self.solver.add(Sum([
                    If(
                        And(
                            self.tau_week_start[i] <= timeslot.week,
                            timeslot.week <= self.tau_week_end[i],
                            self.tau_week_shift[i] == timeslot.week % course.week_intensity,
                            self.tau_day[i] == timeslot.day,
                            self.tau_class_start[i] <= timeslot.class_number,
                            timeslot.class_number <= self.tau_class_end[i]
                        ),
                        1,
                        0
                    )
                    for i, course in enumerate(self.courses) if course.lecturer == lecturer and filter_vec[i]
                ]) <= 1)

        # Valid classrooms constraint
        for i, course in enumerate(self.courses):
            if course.valid_classrooms is not None:
                constraint_list = []
                for valid_classroom_id in course.valid_classrooms:
                    constraint_list.append(self.alpha[i] == valid_classroom_id)
                self.solver.add(Or(*constraint_list))

        # Classroom capacity constraint
        for i, course in enumerate(self.courses):
            for classroom in self.classrooms:
                if course.combined_code is None:
                    self.solver.add(Implies(self.alpha[i] == classroom.id, classroom.capacity >= course.group_size))
                else:
                    total_size = sum([combined_course.group_size for combined_course in self.courses
                                      if combined_course.combined_code == course.combined_code])
                    self.solver.add(Implies(self.alpha[i] == classroom.id, classroom.capacity >= total_size))

        # Classroom equipment constraint
        for i, course in enumerate(self.courses):
            if course.id in self.equipment_map:
                constraint_list = []
                if len(self.equipment_map[course.id]) == 0:
                    # Returning None as there is no classroom with appropriate equipment
                    self.solver.add(False)
                    return None
                for equipped_classroom_id in self.equipment_map[course.id]:
                    constraint_list.append(self.alpha[i] == equipped_classroom_id)
                self.solver.add(Or(*constraint_list))

        # Time interval constraint
        for i, course in enumerate(self.courses):
            if course.timeslot_from is not None:
                timeslot_from = next(timeslot for timeslot in self.timeslots if timeslot.id == course.timeslot_from)
                self.solver.add(And(
                    self.tau_week_start[i] >= timeslot_from.week,
                    self.tau_day[i] >= timeslot_from.day,
                    self.tau_class_start[i] >= timeslot_from.class_number
                ))
            if course.timeslot_to is not None:
                timeslot_to = next(timeslot for timeslot in self.timeslots if timeslot.id == course.timeslot_to)
                self.solver.add(And(
                    self.tau_week_start[i] <= timeslot_to.week,
                    self.tau_day[i] <= timeslot_to.day,
                    self.tau_class_end[i] <= timeslot_to.class_number
                ))

        # Course chain constraint
        chained_courses = {}
        for i, course in enumerate(self.courses):
            if course.chain_code is not None:
                if course.chain_code in chained_courses:
                    chained_courses[course.chain_code].append((i, course))
                else:
                    chained_courses[course.chain_code] = [(i, course)]

        for chain_code, courses in chained_courses.items():
            tau_list = []
            total_length = 0
            for i, course_i in courses:
                tau_list.append(self.tau[i])
                total_length += course_i.block_length
                for j, course_j in courses:
                    self.solver.add(self.tau_day[i] == self.tau_day[j])
                    if course_i.chain_priority > course_j.chain_priority:
                        self.solver.add(self.tau[i] > self.tau[j])
                    elif course_i.chain_priority < course_j.chain_priority:
                        self.solver.add(self.tau[i] < self.tau[j])

            self.solver.add(max(tau_list) - min(tau_list) == total_length - 1)


    def solve(self) -> ([int], [int]):
        check_result = self.solver.check()
        if check_result.r > 0:
            model = self.solver.model()
            alpha_result = [model[self.alpha[i]].as_long() for i, _ in enumerate(self.alpha)]
            tau_result = [model[self.tau[i]].as_long() for i, _ in enumerate(self.tau)]
            return alpha_result, tau_result

    def __repr__(self):
        return repr('Z3NaiveSolver')

# Return minimum of a vector; error if empty
def min(vs):
    m = vs[0]
    for v in vs[1:]:
        m = If(v < m, v, m)
    return m

# Return maximum of a vector; error if empty
def max(vs):
    m = vs[0]
    for v in vs[1:]:
        m = If(v > m, v, m)
    return m