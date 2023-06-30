from dataclasses import dataclass


@dataclass
class ClassroomEquipment:
    id: int
    classroom: int
    equipment_type: int
    amount: int

