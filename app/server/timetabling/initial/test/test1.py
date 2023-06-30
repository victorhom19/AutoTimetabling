from app.server.timetabling.initial.solver.smt.z3.simplified_solver import Z3SimpleSolver
from app.server.timetabling.initial.test.scenarios.custom import custom_scenario
from app.server.timetabling.initial.test.validator import Validator

if __name__ == '__main__':
    scenario = {
        'courses': custom_scenario.courses,
        'classrooms': custom_scenario.classrooms,
        'timeslots': custom_scenario.timeslots,
        'classroom_equipment': custom_scenario.classroom_equipment,
        'required_equipment': custom_scenario.required_equipment
    }

    solver = Z3SimpleSolver(**scenario)

    solver.init_constraints()
    result = solver.solve()
    assert result is not None, "Solver has not found solution"

    alpha, tau = result
    print(alpha, tau)

    is_valid = Validator.validate(**scenario, alpha=alpha, tau=tau)

    assert is_valid