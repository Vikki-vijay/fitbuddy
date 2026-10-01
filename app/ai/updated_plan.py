from google.genai import types

from .gemini_client import get_client

from ..config import settings


def update_workout_plan(
    original_plan,
    feedback,
    goal,
    intensity
):

    if (
        settings.DEMO_MODE
        and not settings.GEMINI_API_KEY
    ):

        return f"""
UPDATED FITBUDDY WORKOUT PLAN

The previous plan has been adjusted based
on the user's feedback.

USER FEEDBACK:

{feedback}


ORIGINAL PLAN:

{original_plan}


ADJUSTMENT:

The workout should be performed at a
comfortable level based on the feedback.

Reduce exercise volume if the user reports
that the plan is too difficult.

Increase gradual progression only when
the current level feels manageable.

Continue to include recovery and rest days.

Always prioritize comfortable exercise form,
hydration, sleep, and recovery.
"""

    prompt = f"""
Update the following 7-day fitness plan
according to the user's feedback.

Goal:
{goal}

Target intensity:
{intensity}


ORIGINAL PLAN:

{original_plan}


USER FEEDBACK:

{feedback}


Requirements:

1. Return a complete Day 1-Day 7 plan.
2. Apply the feedback clearly.
3. Keep at least one recovery/rest day.
4. Keep the plan practical.
5. Do not diagnose medical conditions.
6. Do not prescribe medication.
"""

    client = get_client()

    response = client.models.generate_content(
        model=settings.GEMINI_WORKOUT_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction="""
You are FitBuddy, a cautious general
fitness planning assistant.

Provide safe general wellness guidance.

Do not diagnose medical conditions.
Do not prescribe medical treatment.
""",
            temperature=0.5,
            max_output_tokens=2500
        )
    )

    return (
        response.text
        or
        original_plan
    )