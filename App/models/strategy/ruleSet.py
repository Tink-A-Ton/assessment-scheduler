from typing import Type
from .levelClash import LevelClash
from .programmeLevelClash import ProgrammeLevelClash
from .defaultClash import DefaultClash
from .clashDetection import ClashDetection

PREDEFINED_RULES: dict[str, Type[ClashDetection]] = {
    "rule0": DefaultClash,
    "rule1": LevelClash,
    "rule2": ProgrammeLevelClash,
}
