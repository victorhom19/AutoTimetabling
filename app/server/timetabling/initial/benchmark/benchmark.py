import asyncio
import multiprocessing.pool
import random
import time
from multiprocessing import Pool

import z3
from pebble import ProcessPool

from app.server.timetabling.initial.benchmark.scenarios import \
    benchmark_2_weeks_2_groups_scenario, benchmark_2_weeks_4_groups_scenario, benchmark_2_weeks_6_groups_scenario, \
    benchmark_4_weeks_2_groups_scenario, benchmark_4_weeks_4_groups_scenario, benchmark_4_weeks_6_groups_scenario, \
    benchmark_4_weeks_8_groups_scenario, benchmark_6_weeks_2_groups_scenario, benchmark_6_weeks_4_groups_scenario, \
    benchmark_6_weeks_6_groups_scenario, benchmark_6_weeks_8_groups_scenario, benchmark_6_weeks_10_groups_scenario, \
    benchmark_8_weeks_2_groups_scenario, benchmark_8_weeks_4_groups_scenario, benchmark_8_weeks_6_groups_scenario, \
    benchmark_8_weeks_8_groups_scenario, benchmark_8_weeks_10_groups_scenario, benchmark_8_weeks_12_groups_scenario, \
    benchmark_10_weeks_2_groups_scenario, benchmark_10_weeks_4_groups_scenario, benchmark_10_weeks_6_groups_scenario, \
    benchmark_10_weeks_8_groups_scenario, benchmark_10_weeks_10_groups_scenario, benchmark_10_weeks_12_groups_scenario, \
    benchmark_10_weeks_15_groups_scenario, benchmark_12_weeks_2_groups_scenario, benchmark_12_weeks_4_groups_scenario, \
    benchmark_12_weeks_6_groups_scenario, benchmark_12_weeks_8_groups_scenario, benchmark_12_weeks_10_groups_scenario, \
    benchmark_12_weeks_12_groups_scenario, benchmark_12_weeks_15_groups_scenario, benchmark_12_weeks_18_groups_scenario, \
    benchmark_14_weeks_2_groups_scenario, benchmark_14_weeks_4_groups_scenario, benchmark_14_weeks_6_groups_scenario, \
    benchmark_14_weeks_8_groups_scenario, benchmark_14_weeks_10_groups_scenario, benchmark_14_weeks_12_groups_scenario, \
    benchmark_14_weeks_15_groups_scenario, benchmark_14_weeks_18_groups_scenario, benchmark_14_weeks_20_groups_scenario, \
    benchmark_16_weeks_2_groups_scenario, benchmark_16_weeks_4_groups_scenario, benchmark_16_weeks_6_groups_scenario, \
    benchmark_16_weeks_8_groups_scenario, benchmark_16_weeks_10_groups_scenario, benchmark_16_weeks_12_groups_scenario, \
    benchmark_16_weeks_15_groups_scenario, benchmark_16_weeks_18_groups_scenario, benchmark_16_weeks_20_groups_scenario, \
    benchmark_16_weeks_24_groups_scenario
from app.server.timetabling.initial.solver.smt.z3.intersection_solver import Z3IntersectionSolver
from app.server.timetabling.initial.solver.smt.z3.naive_solver import Z3NaiveSolver
from app.server.timetabling.initial.solver.smt.z3.simplified_solver import Z3SimpleSolver
from app.server.timetabling.initial.solver.smt.z3.tracing_solver import Z3TracingSolver
from app.server.timetabling.initial.test.validator import Validator
from concurrent.futures._base import TimeoutError

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Benchmark:

    def __init__(self, Solvers):
        self.Solvers = Solvers


    @staticmethod
    def run_solver(scenario, Solver):
        solver = Solver(**scenario)

        print(f'* Running for {Solver}:')

        print(f'\tGenerating constraints...', end='')
        solver.init_constraints()
        print(f'\r\tTotal assertions = {len(solver.solver.assertions())}')
        print('\tSolving...', end='')
        start_time = time.perf_counter()
        try:
            result = solver.solve()
            end_time = time.perf_counter()
            assert result is not None

            alpha, tau = result
            is_valid = Validator.validate(**scenario, alpha=alpha, tau=tau)
            assert is_valid

            print(bcolors.OKGREEN + f'\r\tTotal time = {end_time - start_time:5.2f} seconds\n' + bcolors.ENDC)

            return result
        except AssertionError:

            print(bcolors.FAIL + f'\r\tASSERTION ERROR\n' + bcolors.ENDC)


    def run_w2_g2(self):
        print('SCENARIO 2 WEEKS AND 2 GROUPS:\n')
        scenario = {
            'courses': benchmark_2_weeks_2_groups_scenario.courses,
            'classrooms': benchmark_2_weeks_2_groups_scenario.classrooms,
            'timeslots': benchmark_2_weeks_2_groups_scenario.timeslots,
            'classroom_equipment': benchmark_2_weeks_2_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_2_weeks_2_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w2_g4(self):
        print('SCENARIO 2 WEEKS AND 4 GROUPS:\n')
        scenario = {
            'courses': benchmark_2_weeks_4_groups_scenario.courses,
            'classrooms': benchmark_2_weeks_4_groups_scenario.classrooms,
            'timeslots': benchmark_2_weeks_4_groups_scenario.timeslots,
            'classroom_equipment': benchmark_2_weeks_4_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_2_weeks_4_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w2_g6(self):
        print('SCENARIO 2 WEEKS AND 6 GROUPS:\n')
        scenario = {
            'courses': benchmark_2_weeks_6_groups_scenario.courses,
            'classrooms': benchmark_2_weeks_6_groups_scenario.classrooms,
            'timeslots': benchmark_2_weeks_6_groups_scenario.timeslots,
            'classroom_equipment': benchmark_2_weeks_6_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_2_weeks_6_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w4_g2(self):
        print('SCENARIO 4 WEEKS AND 2 GROUPS:\n')
        scenario = {
            'courses': benchmark_4_weeks_2_groups_scenario.courses,
            'classrooms': benchmark_4_weeks_2_groups_scenario.classrooms,
            'timeslots': benchmark_4_weeks_2_groups_scenario.timeslots,
            'classroom_equipment': benchmark_4_weeks_2_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_4_weeks_2_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w4_g4(self):
        print('SCENARIO 4 WEEKS AND 4 GROUPS:\n')
        scenario = {
            'courses': benchmark_4_weeks_4_groups_scenario.courses,
            'classrooms': benchmark_4_weeks_4_groups_scenario.classrooms,
            'timeslots': benchmark_4_weeks_4_groups_scenario.timeslots,
            'classroom_equipment': benchmark_4_weeks_4_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_4_weeks_4_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w4_g6(self):
        print('SCENARIO 4 WEEKS AND 6 GROUPS:\n')
        scenario = {
            'courses': benchmark_4_weeks_6_groups_scenario.courses,
            'classrooms': benchmark_4_weeks_6_groups_scenario.classrooms,
            'timeslots': benchmark_4_weeks_6_groups_scenario.timeslots,
            'classroom_equipment': benchmark_4_weeks_6_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_4_weeks_6_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w4_g8(self):
        print('SCENARIO 4 WEEKS AND 8 GROUPS:\n')
        scenario = {
            'courses': benchmark_4_weeks_8_groups_scenario.courses,
            'classrooms': benchmark_4_weeks_8_groups_scenario.classrooms,
            'timeslots': benchmark_4_weeks_8_groups_scenario.timeslots,
            'classroom_equipment': benchmark_4_weeks_8_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_4_weeks_8_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w6_g2(self):
        print('SCENARIO 6 WEEKS AND 2 GROUPS:\n')
        scenario = {
            'courses': benchmark_6_weeks_2_groups_scenario.courses,
            'classrooms': benchmark_6_weeks_2_groups_scenario.classrooms,
            'timeslots': benchmark_6_weeks_2_groups_scenario.timeslots,
            'classroom_equipment': benchmark_6_weeks_2_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_6_weeks_2_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w6_g4(self):
        print('SCENARIO 6 WEEKS AND 4 GROUPS:\n')
        scenario = {
            'courses': benchmark_6_weeks_4_groups_scenario.courses,
            'classrooms': benchmark_6_weeks_4_groups_scenario.classrooms,
            'timeslots': benchmark_6_weeks_4_groups_scenario.timeslots,
            'classroom_equipment': benchmark_6_weeks_4_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_6_weeks_4_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w6_g6(self):
        print('SCENARIO 6 WEEKS AND 6 GROUPS:\n')
        scenario = {
            'courses': benchmark_6_weeks_6_groups_scenario.courses,
            'classrooms': benchmark_6_weeks_6_groups_scenario.classrooms,
            'timeslots': benchmark_6_weeks_6_groups_scenario.timeslots,
            'classroom_equipment': benchmark_6_weeks_6_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_6_weeks_6_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w6_g8(self):
        print('SCENARIO 6 WEEKS AND 8 GROUPS:\n')
        scenario = {
            'courses': benchmark_6_weeks_8_groups_scenario.courses,
            'classrooms': benchmark_6_weeks_8_groups_scenario.classrooms,
            'timeslots': benchmark_6_weeks_8_groups_scenario.timeslots,
            'classroom_equipment': benchmark_6_weeks_8_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_6_weeks_8_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w6_g10(self):
        print('SCENARIO 6 WEEKS AND 10 GROUPS:\n')
        scenario = {
            'courses': benchmark_6_weeks_10_groups_scenario.courses,
            'classrooms': benchmark_6_weeks_10_groups_scenario.classrooms,
            'timeslots': benchmark_6_weeks_10_groups_scenario.timeslots,
            'classroom_equipment': benchmark_6_weeks_10_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_6_weeks_10_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w8_g2(self):
        print('SCENARIO 8 WEEKS AND 2 GROUPS:\n')
        scenario = {
            'courses': benchmark_8_weeks_2_groups_scenario.courses,
            'classrooms': benchmark_8_weeks_2_groups_scenario.classrooms,
            'timeslots': benchmark_8_weeks_2_groups_scenario.timeslots,
            'classroom_equipment': benchmark_8_weeks_2_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_8_weeks_2_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w8_g4(self):
        print('SCENARIO 8 WEEKS AND 4 GROUPS:\n')
        scenario = {
            'courses': benchmark_8_weeks_4_groups_scenario.courses,
            'classrooms': benchmark_8_weeks_4_groups_scenario.classrooms,
            'timeslots': benchmark_8_weeks_4_groups_scenario.timeslots,
            'classroom_equipment': benchmark_8_weeks_4_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_8_weeks_4_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w8_g6(self):
        print('SCENARIO 8 WEEKS AND 6 GROUPS:\n')
        scenario = {
            'courses': benchmark_8_weeks_6_groups_scenario.courses,
            'classrooms': benchmark_8_weeks_6_groups_scenario.classrooms,
            'timeslots': benchmark_8_weeks_6_groups_scenario.timeslots,
            'classroom_equipment': benchmark_8_weeks_6_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_8_weeks_6_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w8_g8(self):
        print('SCENARIO 8 WEEKS AND 8 GROUPS:\n')
        scenario = {
            'courses': benchmark_8_weeks_8_groups_scenario.courses,
            'classrooms': benchmark_8_weeks_8_groups_scenario.classrooms,
            'timeslots': benchmark_8_weeks_8_groups_scenario.timeslots,
            'classroom_equipment': benchmark_8_weeks_8_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_8_weeks_8_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w8_g10(self):
        print('SCENARIO 8 WEEKS AND 10 GROUPS:\n')
        scenario = {
            'courses': benchmark_8_weeks_10_groups_scenario.courses,
            'classrooms': benchmark_8_weeks_10_groups_scenario.classrooms,
            'timeslots': benchmark_8_weeks_10_groups_scenario.timeslots,
            'classroom_equipment': benchmark_8_weeks_10_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_8_weeks_10_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w8_g12(self):
        print('SCENARIO 8 WEEKS AND 12 GROUPS:\n')
        scenario = {
            'courses': benchmark_8_weeks_12_groups_scenario.courses,
            'classrooms': benchmark_8_weeks_12_groups_scenario.classrooms,
            'timeslots': benchmark_8_weeks_12_groups_scenario.timeslots,
            'classroom_equipment': benchmark_8_weeks_12_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_8_weeks_12_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w10_g2(self):
        print('SCENARIO 10 WEEKS AND 2 GROUPS:\n')
        scenario = {
            'courses': benchmark_10_weeks_2_groups_scenario.courses,
            'classrooms': benchmark_10_weeks_2_groups_scenario.classrooms,
            'timeslots': benchmark_10_weeks_2_groups_scenario.timeslots,
            'classroom_equipment': benchmark_10_weeks_2_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_10_weeks_2_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w10_g4(self):
        print('SCENARIO 10 WEEKS AND 4 GROUPS:\n')
        scenario = {
            'courses': benchmark_10_weeks_4_groups_scenario.courses,
            'classrooms': benchmark_10_weeks_4_groups_scenario.classrooms,
            'timeslots': benchmark_10_weeks_4_groups_scenario.timeslots,
            'classroom_equipment': benchmark_10_weeks_4_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_10_weeks_4_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w10_g6(self):
        print('SCENARIO 10 WEEKS AND 6 GROUPS:\n')
        scenario = {
            'courses': benchmark_10_weeks_6_groups_scenario.courses,
            'classrooms': benchmark_10_weeks_6_groups_scenario.classrooms,
            'timeslots': benchmark_10_weeks_6_groups_scenario.timeslots,
            'classroom_equipment': benchmark_10_weeks_6_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_10_weeks_6_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w10_g8(self):
        print('SCENARIO 10 WEEKS AND 8 GROUPS:\n')
        scenario = {
            'courses': benchmark_10_weeks_8_groups_scenario.courses,
            'classrooms': benchmark_10_weeks_8_groups_scenario.classrooms,
            'timeslots': benchmark_10_weeks_8_groups_scenario.timeslots,
            'classroom_equipment': benchmark_10_weeks_8_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_10_weeks_8_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w10_g10(self):
        print('SCENARIO 10 WEEKS AND 10 GROUPS:\n')
        scenario = {
            'courses': benchmark_10_weeks_10_groups_scenario.courses,
            'classrooms': benchmark_10_weeks_10_groups_scenario.classrooms,
            'timeslots': benchmark_10_weeks_10_groups_scenario.timeslots,
            'classroom_equipment': benchmark_10_weeks_10_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_10_weeks_10_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w10_g12(self):
        print('SCENARIO 10 WEEKS AND 12 GROUPS:\n')
        scenario = {
            'courses': benchmark_10_weeks_12_groups_scenario.courses,
            'classrooms': benchmark_10_weeks_12_groups_scenario.classrooms,
            'timeslots': benchmark_10_weeks_12_groups_scenario.timeslots,
            'classroom_equipment': benchmark_10_weeks_12_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_10_weeks_12_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w10_g15(self):
        print('SCENARIO 10 WEEKS AND 15 GROUPS:\n')
        scenario = {
            'courses': benchmark_10_weeks_15_groups_scenario.courses,
            'classrooms': benchmark_10_weeks_15_groups_scenario.classrooms,
            'timeslots': benchmark_10_weeks_15_groups_scenario.timeslots,
            'classroom_equipment': benchmark_10_weeks_15_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_10_weeks_15_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w12_g2(self):
        print('SCENARIO 12 WEEKS AND 2 GROUPS:\n')
        scenario = {
            'courses': benchmark_12_weeks_2_groups_scenario.courses,
            'classrooms': benchmark_12_weeks_2_groups_scenario.classrooms,
            'timeslots': benchmark_12_weeks_2_groups_scenario.timeslots,
            'classroom_equipment': benchmark_12_weeks_2_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_12_weeks_2_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w12_g4(self):
        print('SCENARIO 12 WEEKS AND 4 GROUPS:\n')
        scenario = {
            'courses': benchmark_12_weeks_4_groups_scenario.courses,
            'classrooms': benchmark_12_weeks_4_groups_scenario.classrooms,
            'timeslots': benchmark_12_weeks_4_groups_scenario.timeslots,
            'classroom_equipment': benchmark_12_weeks_4_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_12_weeks_4_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w12_g6(self):
        print('SCENARIO 12 WEEKS AND 6 GROUPS:\n')
        scenario = {
            'courses': benchmark_12_weeks_6_groups_scenario.courses,
            'classrooms': benchmark_12_weeks_6_groups_scenario.classrooms,
            'timeslots': benchmark_12_weeks_6_groups_scenario.timeslots,
            'classroom_equipment': benchmark_12_weeks_6_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_12_weeks_6_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w12_g8(self):
        print('SCENARIO 12 WEEKS AND 8 GROUPS:\n')
        scenario = {
            'courses': benchmark_12_weeks_8_groups_scenario.courses,
            'classrooms': benchmark_12_weeks_8_groups_scenario.classrooms,
            'timeslots': benchmark_12_weeks_8_groups_scenario.timeslots,
            'classroom_equipment': benchmark_12_weeks_8_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_12_weeks_8_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w12_g10(self):
        print('SCENARIO 12 WEEKS AND 10 GROUPS:\n')
        scenario = {
            'courses': benchmark_12_weeks_10_groups_scenario.courses,
            'classrooms': benchmark_12_weeks_10_groups_scenario.classrooms,
            'timeslots': benchmark_12_weeks_10_groups_scenario.timeslots,
            'classroom_equipment': benchmark_12_weeks_10_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_12_weeks_10_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w12_g12(self):
        print('SCENARIO 12 WEEKS AND 12 GROUPS:\n')
        scenario = {
            'courses': benchmark_12_weeks_12_groups_scenario.courses,
            'classrooms': benchmark_12_weeks_12_groups_scenario.classrooms,
            'timeslots': benchmark_12_weeks_12_groups_scenario.timeslots,
            'classroom_equipment': benchmark_12_weeks_12_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_12_weeks_12_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w12_g15(self):
        print('SCENARIO 12 WEEKS AND 15 GROUPS:\n')
        scenario = {
            'courses': benchmark_12_weeks_15_groups_scenario.courses,
            'classrooms': benchmark_12_weeks_15_groups_scenario.classrooms,
            'timeslots': benchmark_12_weeks_15_groups_scenario.timeslots,
            'classroom_equipment': benchmark_12_weeks_15_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_12_weeks_15_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w12_g18(self):
        print('SCENARIO 12 WEEKS AND 18 GROUPS:\n')
        scenario = {
            'courses': benchmark_12_weeks_18_groups_scenario.courses,
            'classrooms': benchmark_12_weeks_18_groups_scenario.classrooms,
            'timeslots': benchmark_12_weeks_18_groups_scenario.timeslots,
            'classroom_equipment': benchmark_12_weeks_18_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_12_weeks_18_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w14_g2(self):
        print('SCENARIO 14 WEEKS AND 2 GROUPS:\n')
        scenario = {
            'courses': benchmark_14_weeks_2_groups_scenario.courses,
            'classrooms': benchmark_14_weeks_2_groups_scenario.classrooms,
            'timeslots': benchmark_14_weeks_2_groups_scenario.timeslots,
            'classroom_equipment': benchmark_14_weeks_2_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_14_weeks_2_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w14_g4(self):
        print('SCENARIO 14 WEEKS AND 4 GROUPS:\n')
        scenario = {
            'courses': benchmark_14_weeks_4_groups_scenario.courses,
            'classrooms': benchmark_14_weeks_4_groups_scenario.classrooms,
            'timeslots': benchmark_14_weeks_4_groups_scenario.timeslots,
            'classroom_equipment': benchmark_14_weeks_4_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_14_weeks_4_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w14_g6(self):
        print('SCENARIO 14 WEEKS AND 6 GROUPS:\n')
        scenario = {
            'courses': benchmark_14_weeks_6_groups_scenario.courses,
            'classrooms': benchmark_14_weeks_6_groups_scenario.classrooms,
            'timeslots': benchmark_14_weeks_6_groups_scenario.timeslots,
            'classroom_equipment': benchmark_14_weeks_6_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_14_weeks_6_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w14_g8(self):
        print('SCENARIO 14 WEEKS AND 8 GROUPS:\n')
        scenario = {
            'courses': benchmark_14_weeks_8_groups_scenario.courses,
            'classrooms': benchmark_14_weeks_8_groups_scenario.classrooms,
            'timeslots': benchmark_14_weeks_8_groups_scenario.timeslots,
            'classroom_equipment': benchmark_14_weeks_8_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_14_weeks_8_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w14_g10(self):
        print('SCENARIO 14 WEEKS AND 10 GROUPS:\n')
        scenario = {
            'courses': benchmark_14_weeks_10_groups_scenario.courses,
            'classrooms': benchmark_14_weeks_10_groups_scenario.classrooms,
            'timeslots': benchmark_14_weeks_10_groups_scenario.timeslots,
            'classroom_equipment': benchmark_14_weeks_10_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_14_weeks_10_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w14_g12(self):
        print('SCENARIO 14 WEEKS AND 12 GROUPS:\n')
        scenario = {
            'courses': benchmark_14_weeks_12_groups_scenario.courses,
            'classrooms': benchmark_14_weeks_12_groups_scenario.classrooms,
            'timeslots': benchmark_14_weeks_12_groups_scenario.timeslots,
            'classroom_equipment': benchmark_14_weeks_12_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_14_weeks_12_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w14_g15(self):
        print('SCENARIO 14 WEEKS AND 15 GROUPS:\n')
        scenario = {
            'courses': benchmark_14_weeks_15_groups_scenario.courses,
            'classrooms': benchmark_14_weeks_15_groups_scenario.classrooms,
            'timeslots': benchmark_14_weeks_15_groups_scenario.timeslots,
            'classroom_equipment': benchmark_14_weeks_15_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_14_weeks_15_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w14_g18(self):
        print('SCENARIO 14 WEEKS AND 18 GROUPS:\n')
        scenario = {
            'courses': benchmark_14_weeks_18_groups_scenario.courses,
            'classrooms': benchmark_14_weeks_18_groups_scenario.classrooms,
            'timeslots': benchmark_14_weeks_18_groups_scenario.timeslots,
            'classroom_equipment': benchmark_14_weeks_18_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_14_weeks_18_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w14_g20(self):
        print('SCENARIO 14 WEEKS AND 20 GROUPS:\n')
        scenario = {
            'courses': benchmark_14_weeks_20_groups_scenario.courses,
            'classrooms': benchmark_14_weeks_20_groups_scenario.classrooms,
            'timeslots': benchmark_14_weeks_20_groups_scenario.timeslots,
            'classroom_equipment': benchmark_14_weeks_20_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_14_weeks_20_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w16_g2(self):
        print('SCENARIO 16 WEEKS AND 2 GROUPS:\n')
        scenario = {
            'courses': benchmark_16_weeks_2_groups_scenario.courses,
            'classrooms': benchmark_16_weeks_2_groups_scenario.classrooms,
            'timeslots': benchmark_16_weeks_2_groups_scenario.timeslots,
            'classroom_equipment': benchmark_16_weeks_2_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_16_weeks_2_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w16_g4(self):
        print('SCENARIO 16 WEEKS AND 4 GROUPS:\n')
        scenario = {
            'courses': benchmark_16_weeks_4_groups_scenario.courses,
            'classrooms': benchmark_16_weeks_4_groups_scenario.classrooms,
            'timeslots': benchmark_16_weeks_4_groups_scenario.timeslots,
            'classroom_equipment': benchmark_16_weeks_4_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_16_weeks_4_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w16_g6(self):
        print('SCENARIO 16 WEEKS AND 6 GROUPS:\n')
        scenario = {
            'courses': benchmark_16_weeks_6_groups_scenario.courses,
            'classrooms': benchmark_16_weeks_6_groups_scenario.classrooms,
            'timeslots': benchmark_16_weeks_6_groups_scenario.timeslots,
            'classroom_equipment': benchmark_16_weeks_6_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_16_weeks_6_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w16_g8(self):
        print('SCENARIO 16 WEEKS AND 8 GROUPS:\n')
        scenario = {
            'courses': benchmark_16_weeks_8_groups_scenario.courses,
            'classrooms': benchmark_16_weeks_8_groups_scenario.classrooms,
            'timeslots': benchmark_16_weeks_8_groups_scenario.timeslots,
            'classroom_equipment': benchmark_16_weeks_8_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_16_weeks_8_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w16_g10(self):
        print('SCENARIO 16 WEEKS AND 10 GROUPS:\n')
        scenario = {
            'courses': benchmark_16_weeks_10_groups_scenario.courses,
            'classrooms': benchmark_16_weeks_10_groups_scenario.classrooms,
            'timeslots': benchmark_16_weeks_10_groups_scenario.timeslots,
            'classroom_equipment': benchmark_16_weeks_10_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_16_weeks_10_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w16_g12(self):
        print('SCENARIO 16 WEEKS AND 12 GROUPS:\n')
        scenario = {
            'courses': benchmark_16_weeks_12_groups_scenario.courses,
            'classrooms': benchmark_16_weeks_12_groups_scenario.classrooms,
            'timeslots': benchmark_16_weeks_12_groups_scenario.timeslots,
            'classroom_equipment': benchmark_16_weeks_12_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_16_weeks_12_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w16_g15(self):
        print('SCENARIO 16 WEEKS AND 15 GROUPS:\n')
        scenario = {
            'courses': benchmark_16_weeks_15_groups_scenario.courses,
            'classrooms': benchmark_16_weeks_15_groups_scenario.classrooms,
            'timeslots': benchmark_16_weeks_15_groups_scenario.timeslots,
            'classroom_equipment': benchmark_16_weeks_15_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_16_weeks_15_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w16_g18(self):
        print('SCENARIO 16 WEEKS AND 18 GROUPS:\n')
        scenario = {
            'courses': benchmark_16_weeks_18_groups_scenario.courses,
            'classrooms': benchmark_16_weeks_18_groups_scenario.classrooms,
            'timeslots': benchmark_16_weeks_18_groups_scenario.timeslots,
            'classroom_equipment': benchmark_16_weeks_18_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_16_weeks_18_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w16_g20(self):
        print('SCENARIO 16 WEEKS AND 20 GROUPS:\n')
        scenario = {
            'courses': benchmark_16_weeks_20_groups_scenario.courses,
            'classrooms': benchmark_16_weeks_20_groups_scenario.classrooms,
            'timeslots': benchmark_16_weeks_20_groups_scenario.timeslots,
            'classroom_equipment': benchmark_16_weeks_20_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_16_weeks_20_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def run_w16_g24(self):
        print('SCENARIO 16 WEEKS AND 24 GROUPS:\n')
        scenario = {
            'courses': benchmark_16_weeks_24_groups_scenario.courses,
            'classrooms': benchmark_16_weeks_24_groups_scenario.classrooms,
            'timeslots': benchmark_16_weeks_24_groups_scenario.timeslots,
            'classroom_equipment': benchmark_16_weeks_24_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_16_weeks_24_groups_scenario.required_equipment
        }
        for Solver in self.Solvers:
            with ProcessPool() as pool:
                future = pool.schedule(Benchmark.run_solver, args=[scenario, Solver], timeout=1800)
                try:
                    result = future.result()
                except TimeoutError:
                    print(bcolors.WARNING + '\n\tTIMEOUT EXCEEDED\n' + bcolors.ENDC)
        print(f'--------------------------------------------\n')

    def test(self, Solver):
        print('SCENARIO 16 WEEKS AND 8 GROUPS:\n')
        scenario = {
            'courses': benchmark_16_weeks_8_groups_scenario.courses,
            'classrooms': benchmark_16_weeks_8_groups_scenario.classrooms,
            'timeslots': benchmark_16_weeks_8_groups_scenario.timeslots,
            'classroom_equipment': benchmark_16_weeks_8_groups_scenario.classroom_equipment,
            'required_equipment': benchmark_16_weeks_8_groups_scenario.required_equipment
        }
        random.shuffle(scenario.get('courses'))
        result = self.run_solver(scenario, Solver)
        return result



if __name__ == '__main__':
    benchmark = Benchmark([Z3SimpleSolver])
    pool = Pool(12)
    for result in pool.starmap(Benchmark.test, [(benchmark, Z3SimpleSolver) for _ in range(12)]):
        print(result)

    # benchmark.run_w16_g8()

    # benchmark.run_w2_g2()
    # benchmark.run_w4_g2()
    # benchmark.run_w6_g2()
    # benchmark.run_w8_g2()
    # benchmark.run_w10_g2()
    # benchmark.run_w12_g2()
    # benchmark.run_w14_g2()
    # benchmark.run_w16_g2()
    #
    # benchmark.run_w2_g4()
    # benchmark.run_w4_g4()
    # benchmark.run_w6_g4()
    # benchmark.run_w8_g4()
    # benchmark.run_w10_g4()
    # benchmark.run_w12_g4()
    # benchmark.run_w14_g4()
    # benchmark.run_w16_g4()
    #
    # benchmark.run_w2_g6()
    # benchmark.run_w4_g6()
    # benchmark.run_w6_g6()
    # benchmark.run_w8_g6()
    # benchmark.run_w10_g6()
    # benchmark.run_w12_g6()
    # benchmark.run_w14_g6()
    # benchmark.run_w16_g6()
    #
    # benchmark.run_w4_g8()
    # benchmark.run_w6_g8()
    # benchmark.run_w8_g8()
    # benchmark.run_w10_g8()
    # benchmark.run_w12_g8()
    # benchmark.run_w14_g8()
    # benchmark.run_w16_g8()
    #
    # benchmark.run_w6_g10()
    # benchmark.run_w8_g10()
    # benchmark.run_w10_g10()
    # benchmark.run_w12_g10()
    # benchmark.run_w14_g10()
    # benchmark.run_w16_g10()
    #
    # benchmark.run_w8_g12()
    # benchmark.run_w10_g12()
    # benchmark.run_w12_g12()
    # benchmark.run_w14_g12()
    # benchmark.run_w16_g12()
    #
    # benchmark.run_w10_g15()
    # benchmark.run_w12_g15()
    # benchmark.run_w14_g15()
    # benchmark.run_w16_g15()
    #
    # benchmark.run_w12_g18()
    # benchmark.run_w14_g18()
    # benchmark.run_w16_g18()
    #
    # benchmark.run_w14_g20()
    # benchmark.run_w16_g20()
