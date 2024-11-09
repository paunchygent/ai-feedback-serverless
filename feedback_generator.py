# feedback_generator.py
import openai
from typing import Any 
from models import FeedbackResponse
from openai_utils import get_teacher_feedback, get_editor_revision, format_final_output

def format_final_output(feedback_response: FeedbackResponse) -> str:
    return f"""## Feedback

{feedback_response.teacher_feedback}

## Redaktörens förslag före publicering

{feedback_response.editor_revision}"""

def process_with_openai(student_name: str, essay_text: str, essay_instruction: str, client: Any) -> str:
    # Generate teacher feedback
    teacher_feedback = get_teacher_feedback(
        client=client,
        student_name=student_name,
        essay_text=essay_text,
        essay_instruction=essay_instruction  # Pass instruction
    )

        # Generate editor revision}...")
    editor_revision = get_editor_revision(
        client=client,
        student_name=student_name,
        essay_text=essay_text,
        teacher_feedback=teacher_feedback,
        essay_instruction=essay_instruction  # Pass instruction
    )

    feedback_response = FeedbackResponse(
        teacher_feedback=teacher_feedback,
        editor_revision=editor_revision,
        student_name=student_name
    )

    return format_final_output(feedback_response)