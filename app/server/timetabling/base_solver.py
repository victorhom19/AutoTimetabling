class BaseSolver:

    def __init__(self, courses, classrooms, timeslots, classroom_equipment, required_equipment):

        self.courses = courses
        self.classrooms = classrooms
        self.timeslots = timeslots

        self.classroom_equipment = {}
        for cls_eq in classroom_equipment:
            if cls_eq.classroom in self.classroom_equipment:
                self.classroom_equipment[cls_eq.classroom].append(cls_eq)
            else:
                self.classroom_equipment[cls_eq.classroom] = [cls_eq]

        self.required_equipment = {}
        for req_eq in required_equipment:
            if req_eq.course in self.required_equipment:
                self.required_equipment[req_eq.course].append(req_eq)
            else:
                self.required_equipment[req_eq.course] = [req_eq]

        self.equipment_map = {}
        for course_id, req_eq in self.required_equipment.items():
            self.equipment_map[course_id] = []
            for classroom_id, cls_eq in self.classroom_equipment.items():
                equipped = True
                for req_item in req_eq:
                    filtered_items = [item for item in cls_eq if item.equipment_type == req_item.equipment_type]
                    if len(filtered_items) > 0:
                        cls_item = filtered_items[0]
                    else:
                        cls_item = None

                    if cls_item is None or cls_item.amount < req_item.amount:
                        equipped = False
                if equipped:
                    self.equipment_map[course_id].append(classroom_id)

        self.lecturers = set([course.lecturer for course in self.courses])
        self.groups = set([course.group for course in self.courses])

    def init_constraints(self):
        pass

    def solve(self) -> ([int], [int]):
        pass


class InitialBaseSolver(BaseSolver):
    def __init__(self, courses, classrooms, timeslots, classroom_equipment, required_equipment):
        super().__init__(courses, classrooms, timeslots, classroom_equipment, required_equipment)

    def init_constraints(self):
        super().init_constraints()

    def solve(self) -> ([int], [int]):
        super().solve()
        

class OptimizationBaseSolver(BaseSolver):
    def __init__(self, courses, classrooms, timeslots, classroom_equipment, required_equipment):
        super().__init__(courses, classrooms, timeslots, classroom_equipment, required_equipment)

    def init_constraints(self):
        super().init_constraints()

    def solve(self) -> ([int], [int]):
        super().solve()