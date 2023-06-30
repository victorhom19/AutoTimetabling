import random
from copy import deepcopy
from enum import Enum
import numpy as np

from app.server.timetabling.models.timeslot import Timeslot


class GeneType(Enum):
    INDEPENDENT = 0
    SIMULTANEOUS = 1
    SERIAL = 2


class Gene:

    def __init__(self, locus, gene_type, courses, classrooms, timeslots):
        self.locus = locus
        self.gene_type = gene_type
        self.slot = None
        self.trace = []
        self.locked = False

        self.courses = courses
        self.classrooms = classrooms
        self.timeslots = timeslots

        # Lecturer params
        self.lecturer = self.courses[0].lecturer

        # Group params
        self.groups = [course.group for course in self.courses]
        self.partitions = [course.group_partition for course in self.courses]

        self.group = self.groups[0]
        self.partition = self.partitions[0]

        self.required_capacity = sum([course.group_size * course.group_partition for course in courses])

        # Time params
        self.duration = self.courses[0].duration
        self.week_intensity = self.courses[0].week_intensity
        self.block_length = self.courses[0].block_length
        self.time_from = self.courses[0].time_from
        self.time_to = self.courses[0].time_to

        # Classroom params
        self.valid_classrooms = self.courses[0].valid_classrooms
        self.required_equipment = self.courses[0].required_equipment

        # Building static map
        # 1. Create empty map
        map_shape = (len(classrooms), len(timeslots))
        self.static_map = np.full(map_shape, True)

        # 2. Begin-end constraint
        if self.time_from < 0:
            self.time_from = int(timeslots[0])
        if self.time_to < 0:
            self.time_to = int(timeslots[-1])
        begin_end_vector = [self.time_from <= int(t) <= self.time_to for t in self.timeslots]
        self.static_map = np.logical_and(self.static_map, begin_end_vector)

        # 3. Course completeness constraint (prepare)
        last_slot = deepcopy(self.timeslots[self.time_to])
        last_slot.week -= (self.duration - 1) * self.week_intensity
        self.completeness_vector = [t <= last_slot for t in self.timeslots]

        # 4. Valid classroom constraint
        if len(self.valid_classrooms) > 0:
            valid_classrooms_vector = np.array([[i in self.valid_classrooms for i, _ in enumerate(self.classrooms)]])
            self.static_map = np.logical_and(self.static_map, valid_classrooms_vector.transpose())

        # 5. Classroom capacity constraint
        spacious_classrooms_vector = np.array([[classroom.capacity >= self.required_capacity for classroom in self.classrooms]])
        self.static_map = np.logical_and(self.static_map, spacious_classrooms_vector.transpose())

        # 6. Classroom equipment constraint
        if self.required_equipment is not None:
            equipped_classrooms = []
            for i, classroom in enumerate(self.classrooms):
                all_required_equipment = True
                for r_eq, r_amount in self.required_equipment.items():
                    if (classroom.equipment is None or
                            r_eq not in classroom.equipment or
                            r_amount >= classroom.equipment.get(r_eq)):
                        all_required_equipment = False
                        break
                if all_required_equipment:
                    equipped_classrooms.append(i)

            fully_equipped_classrooms_vector = np.array([[i in equipped_classrooms for i, _ in enumerate(self.classrooms)]])
            self.static_map = np.logical_and(self.static_map, fully_equipped_classrooms_vector.transpose())

    def get_available_slots_map(self, lecturer_map, group_map, classroom_map):
        free_slots_map = deepcopy(self.static_map)

        # 1. Lecturer busyness constraint
        lecturer_state = lecturer_map[self.lecturer]
        free_slots_map = np.logical_and(free_slots_map, lecturer_state)

        # 2. Group busyness constraint
        if self.gene_type == GeneType.INDEPENDENT:
            group_state = group_map[self.group] + self.partition <= 1
            free_slots_map = np.logical_and(free_slots_map, group_state)
        elif self.gene_type == GeneType.SIMULTANEOUS:
            group_states = [group_map[group] + partition <= 1 for group, partition in zip(self.groups, self.partitions)]
            combined_group_state = np.logical_and.reduce(group_states)
            free_slots_map = np.logical_and(free_slots_map, combined_group_state)

        # 3. Classroom busyness constraint
        free_slots_map = np.logical_and(free_slots_map, classroom_map)

        # 4. Course completeness constraint
        # (This constraint is kind of static but it should be applied in the end)
        free_start_slots_map = np.logical_and(free_slots_map, self.completeness_vector)

        # 5. Tracing free slots to find available slots for course beginning
        free_start_slots = np.argwhere(free_start_slots_map)
        shape = free_start_slots_map.shape
        available_slots = np.full(shape, False)
        for f_start_slot in free_start_slots:
            is_available = True
            f_slot_trace = self.trace_course(f_start_slot)
            for traced_slot in f_slot_trace:
                alpha, tau = traced_slot
                if tau >= len(self.timeslots) or not free_slots_map[alpha][tau]:
                    is_available = False
                    break
            if is_available:
                a, t = f_start_slot
                available_slots[a][t] = True

        return available_slots

    def get_available_slots(self, lecturer_map, group_map, classroom_map):
        available_slots_map = self.get_available_slots_map(lecturer_map, group_map, classroom_map)
        return np.argwhere(available_slots_map)

    def get_swap_slot(self, chromosome, lecturer_map, group_map, classroom_map):
        chromosome_copy = deepcopy(chromosome)
        random.shuffle(chromosome_copy)
        for other_gene in chromosome_copy:
            if other_gene.locus != self.locus:
                l_map = deepcopy(lecturer_map)
                g_map = deepcopy(group_map)
                c_map = deepcopy(classroom_map)

                other_gene.clear_trace(l_map, g_map, c_map)
                slots_before = self.get_available_slots_map(lecturer_map, group_map, classroom_map)
                slots_after = self.get_available_slots_map(l_map, g_map, c_map)
                forward_diff = np.logical_xor(slots_after, slots_before)
                forward_swap_slots = np.argwhere(forward_diff)

                if len(forward_swap_slots) > 0:
                    other_gene.set_slot(other_gene.slot, l_map, g_map, c_map)
                    self.clear_trace(l_map, g_map, c_map)
                    slots_before = other_gene.get_available_slots_map(lecturer_map, group_map, classroom_map)
                    slots_after = other_gene.get_available_slots_map(l_map, g_map, c_map)
                    backward_diff = np.logical_xor(slots_after, slots_before)
                    backward_swap_slots = np.argwhere(backward_diff)

                    if len(backward_swap_slots) > 0:
                        f_swap_slot = random.choice(forward_swap_slots)
                        b_swap_slot = random.choice(backward_swap_slots)

                        return f_swap_slot, other_gene.locus, b_swap_slot

        return ()

    def trace_course(self, slot):
        alpha, tau = slot
        slots = []
        for week_shift_i in range(self.duration):
            week_shift = week_shift_i * Timeslot.days_per_week * Timeslot.classes_per_day
            for block_shift in range(self.block_length):
                slots.append((alpha, tau + week_shift + block_shift))
        return slots

    def set_slot(self, slot, lecturer_map, group_map, classroom_map):
        self.slot = slot
        self.trace = self.trace_course(slot)
        for alpha, tau in self.trace:
            lecturer_map[self.lecturer][tau] = False
            if self.gene_type == GeneType.INDEPENDENT:
                group_map[self.group][tau] += self.partition
            elif self.gene_type == GeneType.SIMULTANEOUS:
                for group, partition in zip(self.groups, self.partitions):
                    group_map[group][tau] += partition
            else:
                raise Exception('Invalid gene type')
            classroom_map[alpha][tau] = False

    def remove_slot(self, lecturer_map, group_map, classroom_map):
        self.clear_trace(lecturer_map, group_map, classroom_map)
        self.slot = None
        self.trace = None

    def clear_trace(self, lecturer_map, group_map, classroom_map):
        for alpha, tau in self.trace:
            lecturer_map[self.lecturer][tau] = True
            if self.gene_type == GeneType.INDEPENDENT:
                group_map[self.group][tau] -= self.partition
            elif self.gene_type == GeneType.SIMULTANEOUS:
                for group, partition in zip(self.groups, self.partitions):
                    group_map[group][tau] -= partition
            else:
                raise Exception('Invalid gene type')
            classroom_map[alpha][tau] = True





