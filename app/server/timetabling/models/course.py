from typing import Union, List
from enum import Enum

from dataclasses import dataclass


@dataclass
class Course:
    id: int
    type: int
    discipline: int
    lecturer: int
    group: int
    group_size: int
    part_of: Union[int, None]
    combined_code: Union[int, None]
    duration: int
    week_intensity: int
    block_length: int
    timeslot_from: Union[int, None]
    timeslot_to: Union[int, None]
    chain_code: Union[int, None]
    chain_priority: Union[int, None]
    valid_classrooms: Union[List[int], None]
