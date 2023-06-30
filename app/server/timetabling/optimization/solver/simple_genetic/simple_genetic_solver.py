import copy
import multiprocessing
import random
import time
from enum import Enum
from multiprocessing import Process

import matplotlib.pyplot as plt

import numpy as np
import time

from app.server.timetabling.optimization.solver.simple_genetic.selection_strategies import TruncationSelection
from app.server.timetabling.optimization.solver.simple_genetic.timetable import Timetable
from app.server.timetabling.optimization.solver.io.parser import ParsedInput
from app.server.timetabling.optimization.test.validator import Validator


class SelectionStrategy(Enum):
    TRUNCATION_SELECTION = 1,
    TOURNAMENT_SELECTION = 2


class GeneticSolver:

    def run_graph(self, avg, best):
        print('Graph started')
        fig = plt.figure(figsize=(4, 3))
        ax = plt.subplot()

        plt.xlabel("Iteration")
        plt.ylabel("Fitness")

        plt.xlim(0, 300)

        plt.ion()

        line1, = ax.plot(best, label='Best')
        line2, = ax.plot(avg, label='Average')
        ax.legend()

        ylim_set = False

        while True:
            y1 = list(best)
            y2 = list(avg)

            if not ylim_set and len(y2) > 0:
                plt.ylim(0, 5)
                ylim_set = True

            line1.set_ydata(y1)
            line1.set_xdata(list(range(len(y1))))
            line2.set_ydata(avg)
            line2.set_xdata(list(range(len(y2))))
            plt.show()

            plt.pause(1)



    def solve(self, parsed_input: ParsedInput, strategy):

        manager = multiprocessing.Manager()
        best = manager.list()
        avg = manager.list()


        start_time = time.perf_counter()

        validator = Validator(parsed_input)

        with multiprocessing.Pool(10) as thread_pool:
            population = []

            for result in thread_pool.map(init_individual, [parsed_input for _ in range(strategy.n)]):
                population.append(result)

            iteration_count = 0

            p = Process(target=self.run_graph, args=(avg, best))

            p.start()

            while True:
                iteration_count += 1
                iteration_start_time = time.perf_counter()

                if isinstance(strategy, TruncationSelection):
                    rating = sorted(population, key=lambda x: x.get_fitness())

                    breed_pool = rating[:int(strategy.threshold * len(population))]
                    individuals_to_breed_list = [random.choices(breed_pool, k=2) for _ in range(strategy.breed_number)]
                    for result in thread_pool.map(breed, individuals_to_breed_list):
                        population.append(result)
                else:
                    raise Exception(f'Unknown selection strategy {type(strategy)}')


                for individual in population:
                    for _ in range(strategy.mutation_rate):
                        individual.mutate(strategy.move_to_swap_ratio)

                rating = sorted(population, key=lambda x: x.get_fitness())
                population = rating[:strategy.n]

                valid_count = 0
                for timetable in population:
                    alpha, tau = timetable.as_alpha_tau()
                    if validator.validate(alpha, tau, log=False):
                        valid_count += 1

                rating = sorted(population, key=lambda x: x.get_fitness())
                average_fitness = sum([x.get_fitness() for x in population]) / strategy.n
                best_fitness = rating[0].get_fitness()
                print(f'Total time: {time.perf_counter() - start_time: 5.2f} s')
                print(f'Iteration {iteration_count} - took {time.perf_counter() - iteration_start_time:3.2f} s')
                print(f'Average fitness: {average_fitness}  Best fitness: {best_fitness}')
                print(f'Validation passed: {valid_count} / {strategy.n}')

                best.append(best_fitness)
                avg.append(average_fitness)

                if best_fitness < 0.05 or iteration_count > 33:
                    print(f'Done with best fitness result - {best_fitness}')
                    plt.show(block=True)
                    p.join()
                    return rating[0].as_alpha_tau()


def init_individual(parsed_input):
    print(f'Generated')
    individual = Timetable(
        parsed_input.courses,
        parsed_input.classrooms,
        parsed_input.timeslots
    )
    individual.fill()

    return individual


def breed(timetable_pair):
    first_timetable, second_timetable = timetable_pair
    new_timetable = first_timetable.crossover(second_timetable)
    return new_timetable


def mutate(timetable, mv_to_sw):
    return timetable.mutate(mv_to_sw)
