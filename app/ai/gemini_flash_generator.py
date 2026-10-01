from google.genai import types

from .gemini_client import get_client
from ..config import settings


def demo_nutrition_tip(goal):

    return f"""
FITBUDDY NUTRITION GUIDANCE

Goal: {goal}

General nutrition tips:

- Eat a balanced diet with vegetables and fruits.
- Include adequate protein in your meals.
- Choose whole grains where appropriate.
- Drink enough water throughout the day.
- Limit highly processed foods and excess added sugar.
- Maintain regular meal timing.
- Support your workouts with adequate sleep and recovery.

This is general nutrition information, not medical advice.
"""


def generate_nutrition_tip_with_flash(
    goal,
    intensity
):

    # -------------------------------------------------
    # DEMO MODE
    # -------------------------------------------------

    if settings.DEMO_MODE:

        return demo_nutrition_tip(goal)


    # -------------------------------------------------
    # GEMINI MODE
    # -------------------------------------------------

    if not settings.GEMINI_API_KEY:

        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )


    prompt = f"""
Give general nutrition guidance for a fitness user.

Goal:
{goal}

Workout intensity:
{intensity}

Provide 5-7 practical nutrition tips.

Do not diagnose medical conditions.
Do not prescribe medication.
"""


    client = get_client()


    response = client.models.generate_content(

        model=settings.GEMINI_FAST_MODEL,

        contents=prompt,

        config=types.GenerateContentConfig(

            temperature=0.4,

            max_output_tokens=1000

        )

    )


    return response.text or demo_nutrition_tip(goal)