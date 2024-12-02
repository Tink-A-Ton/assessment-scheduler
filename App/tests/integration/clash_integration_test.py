from datetime import date, time
import os
import logging
import unittest
from typing import Any

from ...database import db
from ...controllers.clash import detect_exam_clash
from ...controllers.exam import create_exam
from ...models.domain.exam import Exam
LOGGER: logging.Logger = logging.getLogger(__name__)

# class ClashIntegrationTests(unittest.TestCase):
#     def test_detect_exam_clash(self) -> None:
#         create_exam("COMP1601", date(2024, 2, 1), time(9, 0), time(11, 0))
#         create_exam("COMP1602", date(2024, 2, 1), time(11, 0), time(13, 0))
#         exam: Exam = Exam.query.get(1)
#         self.assertTrue(detect_exam_clash(exam))
# TODO fix