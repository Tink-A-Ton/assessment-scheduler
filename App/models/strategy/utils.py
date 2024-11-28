from typing import Type
from .defaultClash import DefaultClash, LevelClash, ProgrammeLevelClash
from .clashDetection import ClashDetection

PREDEFINED_RULES: dict[str, Type[ClashDetection]] = {
    "rule0": DefaultClash,
    "rule1": LevelClash,
    "rule2": ProgrammeLevelClash,
}
