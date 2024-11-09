# openai_utils.py
from models import FeedbackResponse  
import openai
import logging
from typing import Any

def get_teacher_feedback(client: Any, student_name: str, essay_text: str, essay_instruction: str) -> str:

    """
    Get feedback from the teacher role.

    Args:
        client: OpenAI client instance
        student_name: Name of the student
        essay_text: Processed essay text
        essay_instruction: Original essay instruction

    Returns:
        str: Teacher's feedback

    Raises:
        Exception: If OpenAI API call fails
    """
    teacher_system_msg = """Du är Hanna Karlsson, rutinerad svensklärare på Hulebäcksgymnasiet. Du undervisar i Svenska 1 på samhällsprogrammet och är mentor för klassen. Dina elever har just börjat ettan och detta är deras första skrivuppgift efter ca en månad på gymnasiet. Din feedbackstil är:
1. Rakt och tydligt vuxentilltal
2. Aldrig töntig, hurtigt eller klyschigt. Du lyfter eleven genom konkreta exempel, aldrig genom onödigt peppiga uttryck eller superlativ.
3. Anpassad för gymnasiekunskaper i grammatik och textkomposition
4. Direkt tilltal.
5. Ge tydliga och resonerande exempel i din feedback.
"""

    teacher_user_msg = f"""Här är en uppsats skriven av {student_name} som svar på den givna uppsatsinstruktionen. Ge feedback enligt instruktionerna och be eleven att noggrant undersöka redaktörens förslag på ändringar i elevens text som följer direkt efter din feedback.

Instruktioner för feedback:
- Börja med "Hej [elevens förnamn]!" följt av ett längre inledande resonemang om uppsatsens innehåll i relation till uppsatsinstruktionerna.
- Du inleder sedan alltid med att direkt kommentera resonerande och insiktfullt uppsatsen i relation till uppsatsinstruktionens bedömningskriterier.
- Sedan nämner du tre specifika exempel på förtjänster i texten där skribenten gör något bra, gärna kopplat till uppsatsinstruktionerna.
- Du går sedan vidare med att nämna två tydligt förklarade förbättringsområden som aldrig får vara stavning eller andra enkla fel. Förbättringsområdena måste alltid vara exemplifierade och tydligt förklarade så att eleven förstår vad du menar
- Använd INGA underrubriker i din feedback förutom "Förtjänster" och "Förbättringsområden".
- Ge genomgåemde flera konkreta exempel och förklaringar i din feedback.
- Efter de specifika exemplen i  "Förtjänster" och "Förbättringsområden" avslutar du genom att hänvisa till redaktörens förslag och hälsa med ditt namn, Hanna.

Uppsatsinstruktion:
{essay_instruction}

Uppsats:
{essay_text}"""

    try:
        teacher_completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": teacher_system_msg},
                {"role": "user", "content": teacher_user_msg}
            ],
            temperature=0.5,
            presence_penalty=0.3,
            frequency_penalty=0.2,
            top_p=0.7,
            max_tokens=2000
        )

        return teacher_completion.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Teacher feedback generation failed for {student_name}: {str(e)}")
        raise

def get_editor_revision(client: Any, student_name: str, essay_text: str, teacher_feedback: str, essay_instruction: str) -> str:

    """
    Get revision from the editor role.

    Args:
        client: OpenAI client instance
        student_name: Name of the student
        essay_text: Processed essay text
        essay_instruction: Original essay instruction
        teacher_feedback: Feedback from the teacher

    Returns:
        str: Editor's revision

    Raises:
        Exception: If OpenAI API call fails
    """
    editor_system_msg = """Du är en professionell redaktör som arbetar för en plattform där unga kan publicera sig. Din uppgift är att:
1. Förbättra texten utan att förändra den grundläggande tonen eller stilen
2. Anpassa grammatik, kohesion och språk enligt professionella standarder
3. Vid eventuella anpassningar källhänvisningarna i brödtext ska du utgå från informationen i uppgiftsinstruktionen. ELeverna ska hänvisa fullständigt i brödtext och behöver inte ha en separat källförteckning. Däremot är det klokt att lyfta in datum för publicering inom paranteser (2024-11-29) för att underlätta läsningen.
3. Behålla författarens unika röst
4. Aldrig skriva något riktat till eleven. Du ska enbart synas, aldrig höras."""

    editor_user_msg = f"""Här är en uppsats som ska redigeras baserat på lärarens feedback och dina professionella insikter.

Uppsatsinstruktion:
{essay_instruction}

Uppsats:
{essay_text}

Lärarens feedback:
{teacher_feedback}

Ge endast den redigerade versionen av texten utan några kommentarer eller förklaringar."""

    try:
        editor_completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": editor_system_msg},
                {"role": "user", "content": editor_user_msg}
            ],
            temperature=0.3,
            top_p=0.8,
            max_tokens=2000
        )

        return editor_completion.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Editor revision failed for {student_name}: {str(e)}")
        raise
    
def format_final_output(feedback_response: FeedbackResponse) -> str:
    return f"""## Feedback

{feedback_response.teacher_feedback}

## Redaktörens förslag före publicering

{feedback_response.editor_revision}"""