import unittest

from app.server.timetabling.base_solver import InitialBaseSolver
from app.server.timetabling.initial.solver.smt.z3.intersection_solver import Z3IntersectionSolver
from app.server.timetabling.initial.solver.smt.z3.naive_solver import Z3NaiveSolver
from app.server.timetabling.initial.solver.smt.z3.simplified_solver import Z3SimpleSolver
from app.server.timetabling.initial.solver.smt.z3.tracing_solver import Z3TracingSolver
from app.server.timetabling.initial.test.scenarios.classroom_capacity import classroom_capacity_scenario_1, classroom_capacity_scenario_2, \
    classroom_capacity_scenario_3, classroom_capacity_scenario_4
from app.server.timetabling.initial.test.scenarios.classroom_equipment import classroom_equipment_scenario_1, \
    classroom_equipment_scenario_2
from app.server.timetabling.initial.test.scenarios.classroom_overlaying import classroom_overlaying_scenario_1, \
    classroom_overlaying_scenario_2, classroom_overlaying_scenario_3
from app.server.timetabling.initial.test.scenarios.courses_chain import courses_chain_scenario_1, courses_chain_scenario_2, \
    courses_chain_scenario_3
from app.server.timetabling.initial.test.scenarios.custom import custom_scenario
from app.server.timetabling.initial.test.scenarios.group_overlaying import group_overlaying_scenario_1, group_overlaying_scenario_2, \
    group_overlaying_scenario_3, group_overlaying_scenario_4, group_overlaying_scenario_5
from app.server.timetabling.initial.test.scenarios.lecturer_overlaying import lecturer_overlaying_scenario_1, \
    lecturer_overlaying_scenario_2, lecturer_overlaying_scenario_3
from app.server.timetabling.initial.test.scenarios.time_interval import time_interval_scenario_1, time_interval_scenario_2, \
    time_interval_scenario_3, time_interval_scenario_4, time_interval_scenario_5, time_interval_scenario_6
from app.server.timetabling.initial.test.scenarios.valid_classrooms import valid_classrooms_scenario_1, valid_classrooms_scenario_2
from app.server.timetabling.initial.test.validator import Validator


class SolverTest:

    def setUp(self):
        self.Solver = InitialBaseSolver

    def test_group_overlaying_1(self):
        # Group Overlaying Test #1
        # ---------------------------------------------
        # Scenario forces to assign different timeslots
        # for every course: in other case there will be
        # group overlaying
        # ---------------------------------------------

        scenario = {
            'courses': group_overlaying_scenario_1.courses,
            'classrooms': group_overlaying_scenario_1.classrooms,
            'timeslots': group_overlaying_scenario_1.timeslots,
            'classroom_equipment': group_overlaying_scenario_1.classroom_equipment,
            'required_equipment': group_overlaying_scenario_1.required_equipment
        }

        solver = self.Solver(**scenario)

        solver.init_constraints()
        result = solver.solve()
        assert result is not None, "Solver has not found solution"

        alpha, tau = result

        is_valid = Validator.validate(**scenario, alpha=alpha, tau=tau)

        assert is_valid, "Found solution is invalid"

    def test_group_overlaying_2(self):
        # Group Overlaying Test #2
        # ---------------------------------------------
        # Scenario forces solver to return None
        # as there is no possibility to assign timeslots
        # to courses
        # ---------------------------------------------

        scenario = {
            'courses': group_overlaying_scenario_2.courses,
            'classrooms': group_overlaying_scenario_2.classrooms,
            'timeslots': group_overlaying_scenario_2.timeslots,
            'classroom_equipment': group_overlaying_scenario_2.classroom_equipment,
            'required_equipment': group_overlaying_scenario_2.required_equipment
        }

        solver = self.Solver(**scenario)

        solver.init_constraints()
        result = solver.solve()
        assert result is None

    def test_group_overlaying_3(self):
        # Group Overlaying Test #3
        # ---------------------------------------------
        # Scenario forces solver to fit courses into
        # one day with respect to courses block length.
        # That is because only 3 courses with block length 2
        # will fit into 1 day (which is 6 timeslots long).
        # ---------------------------------------------

        scenario = {
            'courses': group_overlaying_scenario_3.courses,
            'classrooms': group_overlaying_scenario_3.classrooms,
            'timeslots': group_overlaying_scenario_3.timeslots,
            'classroom_equipment': group_overlaying_scenario_3.classroom_equipment,
            'required_equipment': group_overlaying_scenario_3.required_equipment
        }

        solver = self.Solver(**scenario)

        solver.init_constraints()
        result = solver.solve()
        assert result is not None, "Solver has not found solution"

        alpha, tau = result

        is_valid = Validator.validate(**scenario, alpha=alpha, tau=tau)

        assert is_valid, "Found solution is invalid"

    def test_group_overlaying_4(self):
        # Group Overlaying Test #4
        # ---------------------------------------------
        # Scenario forces solver to fit courses into
        # one day with respect to courses partition.
        # That is because 12 courses with partition of 0.5
        # could fit in 1 day (which is 6 classes)
        # ---------------------------------------------

        scenario = {
            'courses': group_overlaying_scenario_4.courses,
            'classrooms': group_overlaying_scenario_4.classrooms,
            'timeslots': group_overlaying_scenario_4.timeslots,
            'classroom_equipment': group_overlaying_scenario_4.classroom_equipment,
            'required_equipment': group_overlaying_scenario_4.required_equipment
        }

        solver = self.Solver(**scenario)

        solver.init_constraints()
        result = solver.solve()
        assert result is not None, "Solver has not found solution"

        alpha, tau = result

        is_valid = Validator.validate(**scenario, alpha=alpha, tau=tau)

        assert is_valid, "Found solution is invalid"

    def test_group_overlaying_5(self):
        # Group Overlaying Test #5
        # ---------------------------------------------
        # Scenario forces solver to return None as
        # it can't fit courses.
        # That is because 12 courses with partition of 0.5
        # could fit in 1 day (which is 6 classes)
        # ---------------------------------------------

        scenario = {
            'courses': group_overlaying_scenario_5.courses,
            'classrooms': group_overlaying_scenario_5.classrooms,
            'timeslots': group_overlaying_scenario_5.timeslots,
            'classroom_equipment': group_overlaying_scenario_5.classroom_equipment,
            'required_equipment': group_overlaying_scenario_5.required_equipment
        }

        solver = self.Solver(**scenario)

        solver.init_constraints()
        result = solver.solve()
        assert result is None, "Solver has found solution when it should not exist"

    def test_classroom_overlaying_1(self):
        # Classroom Overlaying Test #1
        # ---------------------------------------------
        # Scenario forces solver to assign different
        # classrooms for courses: in other case there
        # will be classroom overlaying
        # ---------------------------------------------

        scenario = {
            'courses': classroom_overlaying_scenario_1.courses,
            'classrooms': classroom_overlaying_scenario_1.classrooms,
            'timeslots': classroom_overlaying_scenario_1.timeslots,
            'classroom_equipment': classroom_overlaying_scenario_1.classroom_equipment,
            'required_equipment': classroom_overlaying_scenario_1.required_equipment
        }

        solver = self.Solver(**scenario)

        solver.init_constraints()
        result = solver.solve()
        assert result is not None, "Solver has not found solution"

        alpha, tau = result

        is_valid = Validator.validate(**scenario, alpha=alpha, tau=tau)

        assert is_valid, "Found solution is invalid"

    def test_classroom_overlaying_2(self):
        # Classroom Overlaying Test #2
        # ---------------------------------------------
        # Scenario forces solver to return None as
        # there is no possibility to fit 12 courses in
        # 1 day (which is 6 classes long) with
        # only 1 classroom
        # ---------------------------------------------

        scenario = {
            'courses': classroom_overlaying_scenario_2.courses,
            'classrooms': classroom_overlaying_scenario_2.classrooms,
            'timeslots': classroom_overlaying_scenario_2.timeslots,
            'classroom_equipment': classroom_overlaying_scenario_2.classroom_equipment,
            'required_equipment': classroom_overlaying_scenario_2.required_equipment
        }

        solver = self.Solver(**scenario)

        solver.init_constraints()
        result = solver.solve()
        assert result is None, "Solver has found solution when it should not exist"

    def test_classroom_overlaying_3(self):
        # Classroom Overlaying Test #3
        # ---------------------------------------------
        # Scenario forces solver to fit all 3 courses
        # into single timeslot as these courses are
        # share same combined code
        # ---------------------------------------------

        scenario = {
            'courses': classroom_overlaying_scenario_3.courses,
            'classrooms': classroom_overlaying_scenario_3.classrooms,
            'timeslots': classroom_overlaying_scenario_3.timeslots,
            'classroom_equipment': classroom_overlaying_scenario_3.classroom_equipment,
            'required_equipment': classroom_overlaying_scenario_3.required_equipment
        }

        solver = self.Solver(**scenario)

        solver.init_constraints()
        result = solver.solve()
        assert result is not None, "Solver has not found solution"

        alpha, tau = result

        is_valid = Validator.validate(**scenario, alpha=alpha, tau=tau)

        assert is_valid, "Found solution is invalid"

    def test_lecturer_overlaying_1(self):
        # Lecturer Overlaying Test #1
        # ---------------------------------------------
        # Scenario forces solver to use all
        # available timeslots (6 slots) as
        # all courses are held by a single
        # lecturer. Thus the only way to get
        # valid timetable is to separate courses
        # among whole day.
        # ---------------------------------------------

        scenario = {
            'courses': lecturer_overlaying_scenario_1.courses,
            'classrooms': lecturer_overlaying_scenario_1.classrooms,
            'timeslots': lecturer_overlaying_scenario_1.timeslots,
            'classroom_equipment': lecturer_overlaying_scenario_1.classroom_equipment,
            'required_equipment': lecturer_overlaying_scenario_1.required_equipment
        }

        solver = self.Solver(**scenario)

        solver.init_constraints()
        result = solver.solve()
        assert result is not None, "Solver has not found solution"

        alpha, tau = result

        is_valid = Validator.validate(**scenario, alpha=alpha, tau=tau)

        assert is_valid, "Found solution is invalid"

    def test_lecturer_overlaying_2(self):
        # Lecturer Overlaying Test #2
        # ---------------------------------------------
        # Scenario forces solver to return None
        # as there is no possibility to fit
        # 12 courses which are held by a same lecturer
        # in a single day.
        # ---------------------------------------------

        scenario = {
            'courses': lecturer_overlaying_scenario_2.courses,
            'classrooms': lecturer_overlaying_scenario_2.classrooms,
            'timeslots': lecturer_overlaying_scenario_2.timeslots,
            'classroom_equipment': lecturer_overlaying_scenario_2.classroom_equipment,
            'required_equipment': lecturer_overlaying_scenario_2.required_equipment
        }

        solver = self.Solver(**scenario)

        solver.init_constraints()
        result = solver.solve()
        assert result is None, "Solver has found solution when it should not exist"

    def test_lecturer_overlaying_3(self):
        # Lecturer Overlaying Test #3
        # ---------------------------------------------
        # Scenario forces solver fit all
        # of 3 courses into single timeslot and
        # classroom because these courses share same
        # combined code and thus this is not counted
        # as lecturer overlaying.
        # ---------------------------------------------

        scenario = {
            'courses': lecturer_overlaying_scenario_3.courses,
            'classrooms': lecturer_overlaying_scenario_3.classrooms,
            'timeslots': lecturer_overlaying_scenario_3.timeslots,
            'classroom_equipment': lecturer_overlaying_scenario_3.classroom_equipment,
            'required_equipment': lecturer_overlaying_scenario_3.required_equipment
        }

        solver = self.Solver(**scenario)

        solver.init_constraints()
        result = solver.solve()
        assert result is not None, "Solver has not found solution"

        alpha, tau = result

        is_valid = Validator.validate(**scenario, alpha=alpha, tau=tau)

        assert is_valid, "Found solution is invalid"

    def test_valid_classrooms_1(self):
        # Valid Classrooms Test #1
        # ---------------------------------------------
        # Scenario forces solver to use only explicitly
        # specified classrooms for courses.
        # ---------------------------------------------

        scenario = {
            'courses': valid_classrooms_scenario_1.courses,
            'classrooms': valid_classrooms_scenario_1.classrooms,
            'timeslots': valid_classrooms_scenario_1.timeslots,
            'classroom_equipment': valid_classrooms_scenario_1.classroom_equipment,
            'required_equipment': valid_classrooms_scenario_1.required_equipment
        }

        solver = self.Solver(**scenario)

        solver.init_constraints()
        result = solver.solve()
        assert result is not None, "Solver has not found solution"

        alpha, tau = result

        is_valid = Validator.validate(**scenario, alpha=alpha, tau=tau)

        assert is_valid, "Found solution is invalid"

    def test_valid_classrooms_2(self):
        # Valid Classrooms Test #2
        # ---------------------------------------------
        # Scenario forces solver to use only explicitly
        # specified classrooms for courses. Thus there
        # is no possible way to fit all courses and
        # solver returns None: only 1 classroom of 2
        # is valid, which not enough to fit all courses.
        # ---------------------------------------------

        scenario = {
            'courses': valid_classrooms_scenario_2.courses,
            'classrooms': valid_classrooms_scenario_2.classrooms,
            'timeslots': valid_classrooms_scenario_2.timeslots,
            'classroom_equipment': valid_classrooms_scenario_2.classroom_equipment,
            'required_equipment': valid_classrooms_scenario_2.required_equipment
        }

        solver = self.Solver(**scenario)

        solver.init_constraints()
        result = solver.solve()
        assert result is None, "Solver has found solution when it should not exist"

    def test_classroom_capacity_1(self):
        # Classroom Capacity Test #1
        # ---------------------------------------------
        # Scenario tests appropriate classroom selection
        # with respect to group size.
        # ---------------------------------------------

        scenario = {
            'courses': classroom_capacity_scenario_1.courses,
            'classrooms': classroom_capacity_scenario_1.classrooms,
            'timeslots': classroom_capacity_scenario_1.timeslots,
            'classroom_equipment': classroom_capacity_scenario_1.classroom_equipment,
            'required_equipment': classroom_capacity_scenario_1.required_equipment
        }

        solver = self.Solver(**scenario)

        solver.init_constraints()
        result = solver.solve()
        assert result is not None, "Solver has not found solution"

        alpha, tau = result

        is_valid = Validator.validate(**scenario, alpha=alpha, tau=tau)

        assert is_valid, "Found solution is invalid"

    def test_classroom_capacity_2(self):
        # Classroom Capacity Test #2
        # ---------------------------------------------
        # Scenario forces solver to return None as
        # there is no available classroom with
        # required capacity.
        # ---------------------------------------------

        scenario = {
            'courses': classroom_capacity_scenario_2.courses,
            'classrooms': classroom_capacity_scenario_2.classrooms,
            'timeslots': classroom_capacity_scenario_2.timeslots,
            'classroom_equipment': classroom_capacity_scenario_2.classroom_equipment,
            'required_equipment': classroom_capacity_scenario_2.required_equipment
        }

        solver = self.Solver(**scenario)

        solver.init_constraints()
        result = solver.solve()
        assert result is None, "Solver has found solution when it should not exist"

    def test_classroom_capacity_3(self):
        # Classroom Capacity Test #3
        # ---------------------------------------------
        # Scenario tests appropriate classroom selection
        # with respect to size of all groups which are
        # participating in course (course is combined).
        # ---------------------------------------------

        scenario = {
            'courses': classroom_capacity_scenario_3.courses,
            'classrooms': classroom_capacity_scenario_3.classrooms,
            'timeslots': classroom_capacity_scenario_3.timeslots,
            'classroom_equipment': classroom_capacity_scenario_3.classroom_equipment,
            'required_equipment': classroom_capacity_scenario_3.required_equipment
        }

        solver = self.Solver(**scenario)

        solver.init_constraints()
        result = solver.solve()
        assert result is not None, "Solver has not found solution"

        alpha, tau = result

        is_valid = Validator.validate(**scenario, alpha=alpha, tau=tau)

        assert is_valid, "Found solution is invalid"

    def test_classroom_capacity_4(self):
        # Classroom Capacity Test #4
        # ---------------------------------------------
        # Scenario forces solver to return None as
        # there is no available classroom which can
        # held students of all groups (course is combined)
        # ---------------------------------------------

        scenario = {
            'courses': classroom_capacity_scenario_4.courses,
            'classrooms': classroom_capacity_scenario_4.classrooms,
            'timeslots': classroom_capacity_scenario_4.timeslots,
            'classroom_equipment': classroom_capacity_scenario_4.classroom_equipment,
            'required_equipment': classroom_capacity_scenario_4.required_equipment
        }

        solver = self.Solver(**scenario)

        solver.init_constraints()
        result = solver.solve()
        assert result is None, "Solver has found solution when it should not exist"

    def test_classroom_equipment_1(self):
        # Classroom Capacity Test #1
        # ---------------------------------------------
        # Scenario tests appropriate classroom selection
        # with respect to required equipment. In this
        # scenario all classrooms have necessary equipment.
        # ---------------------------------------------

        scenario = {
            'courses': classroom_equipment_scenario_1.courses,
            'classrooms': classroom_equipment_scenario_1.classrooms,
            'timeslots': classroom_equipment_scenario_1.timeslots,
            'classroom_equipment': classroom_equipment_scenario_1.classroom_equipment,
            'required_equipment': classroom_equipment_scenario_1.required_equipment
        }

        solver = self.Solver(**scenario)

        solver.init_constraints()
        result = solver.solve()
        assert result is not None, "Solver has not found solution"

        alpha, tau = result

        is_valid = Validator.validate(**scenario, alpha=alpha, tau=tau)

        assert is_valid, "Found solution is invalid"

    def test_classroom_equipment_2(self):
        # Classroom Capacity Test #2
        # ---------------------------------------------
        # Scenario forces solver to return None as
        # there are no classrooms with required amount
        # of equipment.
        # ---------------------------------------------

        scenario = {
            'courses': classroom_equipment_scenario_2.courses,
            'classrooms': classroom_equipment_scenario_2.classrooms,
            'timeslots': classroom_equipment_scenario_2.timeslots,
            'classroom_equipment': classroom_equipment_scenario_2.classroom_equipment,
            'required_equipment': classroom_equipment_scenario_2.required_equipment
        }

        solver = self.Solver(**scenario)

        solver.init_constraints()
        result = solver.solve()
        assert result is None, "Solver has found solution when it should not exist"

    def test_time_interval_1(self):
        # Time Interval Test #1
        # ---------------------------------------------
        # Scenario tests appropriate timeslot selection
        # with respect to time interval constraint.
        # This scenario forces solver to fit courses
        # after timeslot with id 6 (inclusively).
        # ---------------------------------------------

        scenario = {
            'courses': time_interval_scenario_1.courses,
            'classrooms': time_interval_scenario_1.classrooms,
            'timeslots': time_interval_scenario_1.timeslots,
            'classroom_equipment': time_interval_scenario_1.classroom_equipment,
            'required_equipment': time_interval_scenario_1.required_equipment
        }

        solver = self.Solver(**scenario)

        solver.init_constraints()
        result = solver.solve()
        assert result is not None, "Solver has not found solution"

        alpha, tau = result

        is_valid = Validator.validate(**scenario, alpha=alpha, tau=tau)

        assert is_valid, "Found solution is invalid"


    def test_time_interval_2(self):
        # Time Interval Test #1
        # ---------------------------------------------
        # Scenario tests appropriate timeslot selection
        # with respect to time interval constraint.
        # This scenario forces solver to fit courses
        # before timeslot with id 5 (inclusively).
        # ---------------------------------------------

        scenario = {
            'courses': time_interval_scenario_2.courses,
            'classrooms': time_interval_scenario_2.classrooms,
            'timeslots': time_interval_scenario_2.timeslots,
            'classroom_equipment': time_interval_scenario_2.classroom_equipment,
            'required_equipment': time_interval_scenario_2.required_equipment
        }

        solver = self.Solver(**scenario)

        solver.init_constraints()
        result = solver.solve()
        assert result is not None, "Solver has not found solution"

        alpha, tau = result

        is_valid = Validator.validate(**scenario, alpha=alpha, tau=tau)

        assert is_valid, "Found solution is invalid"

    def test_time_interval_3(self):
        # Time Interval Test #3
        # ---------------------------------------------
        # Scenario tests appropriate timeslot selection
        # with respect to time interval constraint.
        # This scenario forces solver to fit courses
        # after timeslot with id 6 and before timeslot
        # with id 11 (inclusively).
        # ---------------------------------------------

        scenario = {
            'courses': time_interval_scenario_3.courses,
            'classrooms': time_interval_scenario_3.classrooms,
            'timeslots': time_interval_scenario_3.timeslots,
            'classroom_equipment': time_interval_scenario_3.classroom_equipment,
            'required_equipment': time_interval_scenario_3.required_equipment
        }

        solver = self.Solver(**scenario)

        solver.init_constraints()
        result = solver.solve()
        assert result is not None, "Solver has not found solution"

        alpha, tau = result

        is_valid = Validator.validate(**scenario, alpha=alpha, tau=tau)

        assert is_valid, "Found solution is invalid"

    def test_time_interval_4(self):
        # Time Interval Test #4
        # ---------------------------------------------
        # Scenario forces solver to return None as
        # there is not enough timeslots which satisfy
        # time interval constraints.
        # ---------------------------------------------

        scenario = {
            'courses': time_interval_scenario_4.courses,
            'classrooms': time_interval_scenario_4.classrooms,
            'timeslots': time_interval_scenario_4.timeslots,
            'classroom_equipment': time_interval_scenario_4.classroom_equipment,
            'required_equipment': time_interval_scenario_4.required_equipment
        }

        solver = self.Solver(**scenario)

        solver.init_constraints()
        result = solver.solve()
        assert result is None, "Solver has found solution when it should not exist"

    def test_time_interval_5(self):
        # Time Interval Test #5
        # ---------------------------------------------
        # Scenario forces solver to return None as
        # there is not enough timeslots which satisfy
        # time interval constraints.
        # ---------------------------------------------

        scenario = {
            'courses': time_interval_scenario_5.courses,
            'classrooms': time_interval_scenario_5.classrooms,
            'timeslots': time_interval_scenario_5.timeslots,
            'classroom_equipment': time_interval_scenario_5.classroom_equipment,
            'required_equipment': time_interval_scenario_5.required_equipment
        }

        solver = self.Solver(**scenario)

        solver.init_constraints()
        result = solver.solve()
        assert result is None, "Solver has found solution when it should not exist"

    def test_time_interval_6(self):
        # Time Interval Test #6
        # ---------------------------------------------
        # Scenario forces solver to return None as
        # there is not enough timeslots which satisfy
        # time interval constraints.
        # ---------------------------------------------

        scenario = {
            'courses': time_interval_scenario_6.courses,
            'classrooms': time_interval_scenario_6.classrooms,
            'timeslots': time_interval_scenario_6.timeslots,
            'classroom_equipment': time_interval_scenario_6.classroom_equipment,
            'required_equipment': time_interval_scenario_6.required_equipment
        }

        solver = self.Solver(**scenario)

        solver.init_constraints()
        result = solver.solve()
        assert result is None, "Solver has found solution when it should not exist"

    def test_courses_chain_1(self):
        # Courses Chain Test #1
        # ---------------------------------------------
        # Scenario forces solver to fit courses in
        # explicit order which is defined by
        # chain code and chain priority
        # ---------------------------------------------

        scenario = {
            'courses': courses_chain_scenario_1.courses,
            'classrooms': courses_chain_scenario_1.classrooms,
            'timeslots': courses_chain_scenario_1.timeslots,
            'classroom_equipment': courses_chain_scenario_1.classroom_equipment,
            'required_equipment': courses_chain_scenario_1.required_equipment
        }

        solver = self.Solver(**scenario)

        solver.init_constraints()
        result = solver.solve()
        assert result is not None, "Solver has not found solution"

        alpha, tau = result

        is_valid = Validator.validate(**scenario, alpha=alpha, tau=tau)

        assert is_valid, "Found solution is invalid"


    def test_courses_chain_2(self):
        # Courses Chain Test #2
        # ---------------------------------------------
        # Scenario forces solver to fit courses in
        # explicit order which is defined by
        # chain code and chain priority
        # ---------------------------------------------

        scenario = {
            'courses': courses_chain_scenario_2.courses,
            'classrooms': courses_chain_scenario_2.classrooms,
            'timeslots': courses_chain_scenario_2.timeslots,
            'classroom_equipment': courses_chain_scenario_2.classroom_equipment,
            'required_equipment': courses_chain_scenario_2.required_equipment
        }

        solver = self.Solver(**scenario)

        solver.init_constraints()
        result = solver.solve()
        assert result is not None, "Solver has not found solution"

        alpha, tau = result

        is_valid = Validator.validate(**scenario, alpha=alpha, tau=tau)

        assert is_valid, "Found solution is invalid"

    def test_courses_chain_3(self):
        # Courses Chain Test #3
        # ---------------------------------------------
        # Scenario forces solver to return None as
        # there is no possible way to fit courses in
        # specified order (course that should be last
        # in chain also must be held until the
        # middle of the day and that is contradictory)
        # ---------------------------------------------

        scenario = {
            'courses': courses_chain_scenario_3.courses,
            'classrooms': courses_chain_scenario_3.classrooms,
            'timeslots': courses_chain_scenario_3.timeslots,
            'classroom_equipment': courses_chain_scenario_3.classroom_equipment,
            'required_equipment': courses_chain_scenario_3.required_equipment
        }

        solver = self.Solver(**scenario)

        solver.init_constraints()
        result = solver.solve()
        assert result is None, "Solver has found solution when it should not exist"


class Z3NaiveSolverTest(SolverTest, unittest.TestCase):
    def setUp(self):
        self.Solver = Z3NaiveSolver


class Z3TracingSolverTest(SolverTest, unittest.TestCase):
    def setUp(self):
        self.Solver = Z3TracingSolver


class Z3IntersectionSolverTest(SolverTest, unittest.TestCase):
    def setUp(self):
        self.Solver = Z3IntersectionSolver


class Z3SimpleSolverTest(SolverTest, unittest.TestCase):
    def setUp(self):
        self.Solver = Z3SimpleSolver


