from google.genai import types

from .gemini_client import get_client
from ..config import settings


SYSTEM_INSTRUCTION = """
You are FitBuddy, an AI fitness planning assistant.

Provide practical general fitness and wellness guidance.

Do not diagnose diseases or medical conditions.

Do not prescribe medication.

Do not recommend dangerous or extreme diets.

Do not claim that a workout plan is medically individualized.

Encourage the user to consult a qualified professional
when they have injuries, pregnancy, chronic conditions,
severe pain, eating disorders, or other medical concerns.
"""


def demo_workout(
    username,
    age,
    weight,
    goal,
    intensity
):

    return f"""
FITBUDDY - 7 DAY WORKOUT PLAN

User:
{username}

Age:
{age}

Weight:
{weight} kg

Goal:
{goal}

Intensity:
{intensity}


========================
DAY 1 - FULL BODY
========================

Warm-up:
5-10 minutes of easy walking.

Workout:
• Squats - 3 x 10
• Push-ups - 3 x 8
• Glute bridges - 3 x 12
• Bodyweight rows - 3 x 10

Recovery:
60-90 seconds between sets.

Cooldown:
5 minutes of easy stretching.


========================
DAY 2 - CARDIO
========================

Warm-up:
5 minutes easy walking.

Workout:
25-30 minutes brisk walking,
cycling, or comfortable cardio.

Recovery:
Hydrate and walk slowly for a few minutes.

Cooldown:
5 minutes.


========================
DAY 3 - RECOVERY
========================

Activity:
20-30 minutes gentle walking.

Mobility:
Light stretching.

Focus:
Recovery and sleep.


========================
DAY 4 - LOWER BODY
========================

Warm-up:
5-10 minutes.

Workout:
• Lunges - 3 x 8 each side
• Hip hinges - 3 x 10
• Calf raises - 3 x 15
• Plank - 3 x 30 seconds

Cooldown:
5 minutes.


========================
DAY 5 - UPPER BODY
========================

Warm-up:
Shoulder and arm mobility.

Workout:
• Incline push-ups - 3 x 10
• Rows - 3 x 10
• Shoulder press - 3 x 10
• Bird dog - 3 x 8 each side

Cooldown:
5 minutes.


========================
DAY 6 - CARDIO + MOBILITY
========================

Workout:

20-30 minutes easy cardio.

Then:

10 minutes gentle mobility.

Keep the effort comfortable.


========================
DAY 7 - REST
========================

Take a rest day.

Focus on:

• Hydration
• Sleep
• Normal balanced meals
• Gentle movement if comfortable


GENERAL NOTE

Adjust repetitions, duration, and resistance
according to your experience and comfort.
"""


def generate_workout_gemini(
    username,
    age,
    weight,
    goal,
    intensity
):

    # =================================================
    # DEMO MODE
    # =================================================
    # When DEMO_MODE=true, do NOT call Gemini.
    # This allows the application to work even when
    # Gemini API is unavailable.
    # =================================================

    if settings.DEMO_MODE:

        return demo_workout(
            username,
            age,
            weight,
            goal,
            intensity
        )


    # =================================================
    # GEMINI MODE
    # =================================================

    if not settings.GEMINI_API_KEY:

        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Set GEMINI_API_KEY in .env or enable DEMO_MODE."
        )


    prompt = f"""
Create a complete 7-day general fitness plan.

User name:
{username}

Age:
{age}

Weight:
{weight} kg

Fitness goal:
{goal}

Training intensity:
{intensity}

Requirements:

1. Include Day 1 through Day 7.
2. Give each day a clear focus.
3. Include warm-up.
4. Include main workout.
5. Include recovery.
6. Include cooldown.
7. Include at least one recovery/rest day.
8. Keep recommendations practical.
9. Do not provide medical diagnosis.
10. Do not recommend extreme diets.
"""


    client = get_client()


    response = client.models.generate_content(

        model=settings.GEMINI_WORKOUT_MODEL,

        contents=prompt,

        config=types.GenerateContentConfig(

            system_instruction=SYSTEM_INSTRUCTION,

            temperature=0.5,

            max_output_tokens=2500

        )
    )


    return (
        response.text
        or
        "The AI did not return a workout plan."
    )