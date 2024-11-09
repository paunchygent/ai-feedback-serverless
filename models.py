# models.py
from dataclasses import dataclass

@dataclass
class FeedbackResponse:
    teacher_feedback: str
    editor_revision: str
    student_name: str