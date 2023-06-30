from z3 import SolverFor, Int, Or, And, Implies, If

from app.server.timetabling.models.timeslot import CPD, DPW
from app.server.timetabling.base_solver import InitialBaseSolver


class Z3SimpleSolver(InitialBaseSolver):

    def __init__(self, courses, classrooms, timeslots, classroom_equipment, required_equipment):
        super().__init__(courses, classrooms, timeslots, classroom_equipment, required_equipment)

        self.solver = SolverFor('LIA')

        self.alpha = [Int(f'alpha_{i}') for i, _ in enumerate(self.courses)]

        self.tau_w = [Int(f'tau_w_{i}') for i, _ in enumerate(self.courses)]
        self.tau_d = [Int(f'tau_d_{i}') for i, _ in enumerate(self.courses)]
        self.tau_c = [Int(f'tau_c_{i}') for i, _ in enumerate(self.courses)]

        self.tau_w_end = []
        self.tau_c_end = []

        self.START_WEEK = self.timeslots[0].week
        self.END_WEEK = self.timeslots[-1].week

        self.START_DAY = self.timeslots[0].day
        self.END_DAY = self.timeslots[-1].day

        self.START_CLASS = self.timeslots[0].class_number
        self.END_CLASS = self.timeslots[-1].class_number

        for i, course in enumerate(self.courses):
            tau_w = self.tau_w[i]
            tau_we = Int(f'tau_w_end{i}')
            self.solver.add(tau_we == tau_w + (course.duration - 1) * course.week_intensity)
            self.tau_w_end.append(tau_we)

            tau_c = self.tau_c[i]
            tau_ce = Int(f'tau_c_end_{i}')
            self.solver.add(tau_ce == tau_c + course.block_length - 1)
            self.tau_c_end.append(tau_ce)

    def init_constraints(self):
        # Alpha space constraint
        for alpha_el in self.alpha:
            constraint_list = []
            for classroom in self.classrooms:
                constraint_list.append(alpha_el == classroom.id)
            self.solver.add(Or(*constraint_list))

        # Tau space constraint
        for tau_w, tau_d, tau_c in zip(self.tau_w, self.tau_d, self.tau_c):
            self.solver.add(tau_w >= self.START_WEEK)
            self.solver.add(tau_w <= self.END_WEEK)

            self.solver.add(tau_d >= 0)
            self.solver.add(tau_d < DPW)

            self.solver.add(tau_c >= 0)
            self.solver.add(tau_c < CPD)

        # Course completeness constraint
        for i, course in enumerate(self.courses):
            self.solver.add(self.tau_w[i] >= self.START_WEEK)
            self.solver.add(self.tau_w_end[i] <= self.END_WEEK)

            self.solver.add(Implies(
                self.tau_w[i] == self.START_WEEK,
                self.tau_d[i] >= self.START_DAY
            ))

            self.solver.add(Implies(
                self.tau_w_end[i] == self.END_WEEK,
                self.tau_d[i] <= self.END_DAY
            ))

            self.solver.add(Implies(
                And(
                    self.tau_w_end[i] == self.START_WEEK,
                    self.tau_d[i] == self.START_DAY
                ),
                self.tau_c[i] >= self.START_CLASS
            ))

            self.solver.add(Implies(
                And(
                    self.tau_w_end[i] == self.END_WEEK,
                    self.tau_d[i] == self.END_DAY
                ),
                self.tau_c_end[i] <= self.END_CLASS
            ))

        # Block course constraint
        for i, course in enumerate(self.courses):
            if course.block_length > 1:
                self.solver.add(self.tau_c_end[i] < CPD)

        # Combined course constraint
        for i, course_i in enumerate(self.courses):
            for j, course_j in enumerate(self.courses):
                if i < j and course_i.combined_code is not None and course_i.combined_code == course_j.combined_code:
                    self.solver.add(self.alpha[i] == self.alpha[j])
                    self.solver.add(self.tau_w[i] == self.tau_w[j])
                    self.solver.add(self.tau_d[i] == self.tau_d[j])
                    self.solver.add(self.tau_c[i] == self.tau_c[j])

        # Group overlaying constraint
        for i, course_i in enumerate(self.courses):
            for j, course_j in enumerate(self.courses):
                if i < j and course_i.group == course_j.group or \
                        course_i.part_of == course_j.group or course_j.part_of == course_i.group:
                    self.solver.add(Or(
                        self.tau_c[i] > self.tau_c_end[j],
                        self.tau_c[j] > self.tau_c_end[i],
                        self.tau_d[i] != self.tau_d[j],
                        self.tau_w[i] > self.tau_w_end[j],
                        self.tau_w[j] > self.tau_w_end[i],
                    ))

        # Classroom overlaying constraint
        for i, course_i in enumerate(self.courses):
            for j, course_j in enumerate(self.courses):
                if i < j and course_i.combined_code is None or course_i.combined_code != course_j.combined_code:
                    self.solver.add(Implies(
                        self.alpha[i] == self.alpha[j],

                        Or(
                            self.tau_c[i] > self.tau_c_end[j],
                            self.tau_c[j] > self.tau_c_end[i],
                            self.tau_d[i] != self.tau_d[j],
                            self.tau_w[i] > self.tau_w_end[j],
                            self.tau_w[j] > self.tau_w_end[i]
                        )
                    ))

        # Lecturer overlaying constraint
        for i, course_i in enumerate(self.courses):
            for j, course_j in enumerate(self.courses):
                if i < j and course_i.lecturer == course_j.lecturer:
                    if course_i.combined_code is None or course_i.combined_code != course_j.combined_code:
                        self.solver.add(Or(
                            self.tau_c[i] > self.tau_c_end[j],
                            self.tau_c[j] > self.tau_c_end[i],
                            self.tau_d[i] != self.tau_d[j],
                            self.tau_w[i] > self.tau_w_end[j],
                            self.tau_w[j] > self.tau_w_end[i]
                        ))

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
                timeslot_from = next(
                    timeslot for timeslot in self.timeslots if timeslot.id == course.timeslot_from)
                self.solver.add(And(
                    self.tau_w[i] >= timeslot_from.week,
                    self.tau_d[i] >= timeslot_from.day,
                    self.tau_c[i] >= timeslot_from.class_number
                ))

            if course.timeslot_to is not None:
                timeslot_to = next(timeslot for timeslot in self.timeslots if timeslot.id == course.timeslot_to)
                self.solver.add(And(
                    self.tau_w_end[i] <= timeslot_to.week,
                    self.tau_d[i] <= timeslot_to.day,
                    self.tau_c_end[i] <= timeslot_to.class_number
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
            tau_c_list = []
            total_length = 0
            for i, course_i in courses:
                tau_c_list.append(self.tau_c[i])
                total_length += course_i.block_length
                for j, course_j in courses:
                    self.solver.add(self.tau_w[i] == self.tau_w[j])
                    self.solver.add(self.tau_d[i] == self.tau_d[j])
                    if course_i.chain_priority > course_j.chain_priority:
                        self.solver.add(self.tau_c[i] > self.tau_c[j])
                    elif course_i.chain_priority < course_j.chain_priority:
                        self.solver.add(self.tau_c[i] < self.tau_c[j])

            self.solver.add(max(tau_c_list) - min(tau_c_list) == total_length - 1)


    def solve(self) -> ([int], [int]):
        check_result = self.solver.check()
        if check_result.r > 0:
            model = self.solver.model()
            alpha_result = [model[self.alpha[i]].as_long() for i, _ in enumerate(self.alpha)]
            tau_w_result = [model[self.tau_w[i]].as_long() for i, _ in enumerate(self.tau_w)]
            tau_d_result = [model[self.tau_d[i]].as_long() for i, _ in enumerate(self.tau_d)]
            tau_c_result = [model[self.tau_c[i]].as_long() for i, _ in enumerate(self.tau_c)]

            # Conversion to alpha-tau representation
            tau_result = []
            for i, _ in enumerate(self.courses):
                tau_result.append(tau_w_result[i] * DPW * CPD + tau_d_result[i] * CPD + tau_c_result[i])

            return alpha_result, tau_result

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