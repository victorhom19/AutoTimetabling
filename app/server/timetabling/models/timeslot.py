from dataclasses import dataclass


CPD = 6  # Classes per day
DPW = 6  # Days per week


@dataclass
class Timeslot:
    id: int
    week: int
    day: int
    class_number: int

    def __int__(self):
        return self.week * DPW * CPD + self.day * CPD + self.class_number
