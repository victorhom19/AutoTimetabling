import typing
from dataclasses import dataclass
from enum import Enum


@dataclass
class Classroom:
    id: int
    capacity: int

