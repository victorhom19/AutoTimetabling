from dataclasses import dataclass


@dataclass
class RequiredEquipment:
    id: int
    course: int
    equipment_type: int
    amount: int

