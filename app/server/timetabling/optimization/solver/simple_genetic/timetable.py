import random
from copy import deepcopy
from enum import Enum
from itertools import groupby

import numpy as np

from app.server.timetabling.optimization.solver.simple_genetic.gene import Gene, GeneType
from app.server.timetabling.models.timeslot import Timeslot


class CourseBlockType(Enum):
    PCB_COURSE = 0
    PC_COURSE = 1
    PB_COURSE = 2
    P_COURSE = 3
    ICB_COURSE = 4
    IB_COURSE = 5
    IC_COURSE = 6
    I_COURSE = 7

class Timetable:


    def __init__(self, courses, classrooms, timeslots):
        self.courses = courses
        for i, course in enumerate(courses):
            course.index = i
        self.classrooms = classrooms
        self.timeslots = timeslots

        self.chromosome = []

        lecturers = sorted(set([course.lecturer for course in self.courses]))
        groups = sorted(set([course.group for course in self.courses]))

        self.lecturer_map = np.full((len(lecturers), len(self.timeslots)), True)
        self.group_map = np.full((len(groups), len(self.timeslots)), 0.0)
        self.classroom_map = np.full((len(self.classrooms), len(self.timeslots)), True)

        self.pcb_courses = []
        self.pc_courses = []
        self.pb_courses = []
        self.p_courses = []
        self.icb_courses = []
        self.ib_courses = []
        self.ic_courses = []
        self.i_courses = []

        for i, course in enumerate(self.courses):
            state = {}
            state['Periodic'] = course.duration > 1
            state['Combined'] = course.combined_code >= 0
            state['Block'] = course.block_length > 1

            if state['Periodic']:
                if state['Combined']:
                    if state['Block']:
                        self.pcb_courses.append(course)
                    else:
                        self.pc_courses.append(course)
                else:
                    if state['Block']:
                        self.pb_courses.append(course)
                    else:
                        self.p_courses.append(course)
            else:
                if state['Combined']:
                    if state['Block']:
                        self.icb_courses.append(course)
                    else:
                        self.ic_courses.append(course)
                else:
                    if state['Block']:
                        self.ib_courses.append(course)
                    else:
                        self.i_courses.append(course)

    def lock_existing_genes(self):
        for gene in self.chromosome:
            gene.locked = True

    def fill_with_type(self, type):
        if type == CourseBlockType.PCB_COURSE:
            courses = self.pcb_courses
        elif type == CourseBlockType.PB_COURSE:
            courses = self.pb_courses
        elif type == CourseBlockType.PC_COURSE:
            courses = self.pc_courses
        elif type == CourseBlockType.P_COURSE:
            courses = self.p_courses
        elif type == CourseBlockType.ICB_COURSE:
            courses = self.icb_courses
        elif type == CourseBlockType.IB_COURSE:
            courses = self.ib_courses
        elif type == CourseBlockType.IC_COURSE:
            courses = self.ic_courses
        else:
            courses = self.i_courses

        block = sorted(courses, key=lambda x: x.combined_code)
        for _, courses_iter in groupby(block, key=lambda x: x.combined_code):
            courses = list(courses_iter)
            if courses[0].combined_code >= 0:
                gene_type = GeneType.SIMULTANEOUS
                self.create_gene(gene_type, courses)
            else:
                gene_type = GeneType.INDEPENDENT
                for course in courses:
                    self.create_gene(gene_type, [course])



    def fill(self):
        priority_list = [
            self.pcb_courses,
            self.pc_courses,
            self.pb_courses,
            self.p_courses,
            self.icb_courses,
            self.ib_courses,
            self.ic_courses,
            self.i_courses
        ]
        for block in priority_list:
            block = sorted(block, key=lambda x: x.combined_code)
            for _, courses_iter in groupby(block, key=lambda x: x.combined_code):
                courses = list(courses_iter)
                if courses[0].combined_code >= 0:
                    gene_type = GeneType.SIMULTANEOUS
                    self.create_gene(gene_type, courses)
                else:
                    gene_type = GeneType.INDEPENDENT
                    for course in courses:
                        self.create_gene(gene_type, [course])

        # for course in self.courses:
        #     self.create_gene(GeneType.INDEPENDENT, [course])


    def create_gene(self, gene_type, courses):
        gene = Gene(
            locus=len(self.chromosome),
            gene_type=gene_type,
            courses=courses,
            classrooms=self.classrooms,
            timeslots=self.timeslots
        )

        self.chromosome.append(gene)
        slots = gene.get_available_slots(self.lecturer_map, self.group_map, self.classroom_map)
        selected_slot = random.choice(slots)
        gene.set_slot(
            slot=selected_slot,
            lecturer_map=self.lecturer_map,
            group_map=self.group_map,
            classroom_map=self.classroom_map
        )

    def get_fitness(self):
        w1 = 1
        w2 = 0.01

        se = np.array([])
        for j, group_state in enumerate(self.group_map):
            total_courses_count = len([course for course in self.courses if course.group == j])
            days_number = len(self.timeslots) // Timeslot.classes_per_day
            M = total_courses_count / days_number

            for day in range(days_number):
                courses_per_day_count = 0
                for t in range(Timeslot.classes_per_day):
                    if group_state[day + t]:
                        courses_per_day_count += 1
                se = np.append(se, (M - courses_per_day_count) ** 2)
        mse = np.sqrt(sum(se) / len(se))


        lecturer_penalty = 0

        for i, slot in enumerate(self.lecturer_map[0]):
            if i // Timeslot.classes_per_day % Timeslot.days_per_week in [0, 1, 3, 4] and not slot:
                lecturer_penalty += 1

        for i, slot in enumerate(self.lecturer_map[1]):
            if i // Timeslot.classes_per_day % Timeslot.days_per_week in [0, 1, 4] and not slot:
                lecturer_penalty += 1

        for i, slot in enumerate(self.lecturer_map[2]):
            if i // Timeslot.classes_per_day % Timeslot.days_per_week in [2, 3, 4] and not slot:
                lecturer_penalty += 1

        for i, slot in enumerate(self.lecturer_map[3]):
            if i // Timeslot.classes_per_day % Timeslot.days_per_week in [0, 1, 2, 3, 4] and not slot:
                lecturer_penalty += 1

        for i, slot in enumerate(self.lecturer_map[4]):
            if i // Timeslot.classes_per_day % Timeslot.days_per_week in [0, 1, 4] and not slot:
                lecturer_penalty += 1

        for i, slot in enumerate(self.lecturer_map[5]):
            if i // Timeslot.classes_per_day % Timeslot.days_per_week in [3, 4] and not slot:
                lecturer_penalty += 1

        # for i, slot in enumerate(self.lecturer_map[7]):
        #     if i // Timeslot.classes_per_day % Timeslot.days_per_week in [1, 4] and not slot:
        #         lecturer_penalty += 1
        #
        # for i, slot in enumerate(self.lecturer_map[8]):
        #     if i // Timeslot.classes_per_day % Timeslot.days_per_week in [0, 1, 3] and not slot:
        #         lecturer_penalty += 1
        #
        # for i, slot in enumerate(self.lecturer_map[9]):
        #     if i // Timeslot.classes_per_day % Timeslot.days_per_week in [3, 5] and not slot:
        #         lecturer_penalty += 1

        return w1 * np.mean(mse) + w2 * lecturer_penalty


    def as_alpha_tau(self):
        extracted_courses = []
        for gene in self.chromosome:
            for course in gene.courses:
                extracted_courses.append((course.index, gene.slot))

        slots = [slot for _, slot in sorted(extracted_courses, key=lambda x: x[0])]
        alpha_vector, tau_vector = list(zip(*slots))
        return alpha_vector, tau_vector

    def mutate(self, move_to_swap_ratio):
        gene = random.choice([gene for gene in self.chromosome if not gene.locked])
        move_mutations = gene.get_available_slots(self.lecturer_map, self.group_map, self.classroom_map)
        if len(move_mutations) > 0 and random.random() < move_to_swap_ratio:
            new_slot = random.choice(move_mutations)
            gene.remove_slot(self.lecturer_map, self.group_map, self.classroom_map)
            gene.set_slot(new_slot, self.lecturer_map, self.group_map, self.classroom_map)
        else:
            swap_res = gene.get_swap_slot(self.chromosome, self.lecturer_map, self.group_map, self.classroom_map)
            if len(swap_res) > 0:
                f_swap_slot, other_gene_locus, b_swap_slot = swap_res
                other_gene = self.chromosome[other_gene_locus]
                gene.remove_slot(self.lecturer_map, self.group_map, self.classroom_map)
                other_gene.remove_slot(self.lecturer_map, self.group_map, self.classroom_map)
                gene.set_slot(f_swap_slot, self.lecturer_map, self.group_map, self.classroom_map)
                other_gene.set_slot(b_swap_slot, self.lecturer_map, self.group_map, self.classroom_map)
        return self

    def crossover(self, other):
        child = deepcopy(self)
        adopt_locus_pool = random.sample([i for i, _ in enumerate(self.chromosome)], len(self.chromosome) // 2)
        for locus in adopt_locus_pool:
            gene = child.chromosome[locus]
            other_gene = other.chromosome[locus]

            gene.clear_trace(child.lecturer_map, child.group_map, child.classroom_map)
            slots = [(alpha, tau) for (alpha, tau) in
                     gene.get_available_slots(child.lecturer_map, child.group_map, child.classroom_map)]
            if tuple(other_gene.slot) in slots:
                gene.set_slot(other_gene.slot, child.lecturer_map, child.group_map, child.classroom_map)
            else:
                gene.set_slot(gene.slot, child.lecturer_map, child.group_map, child.classroom_map)
        return child
