from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    Form,
    Request
)

from fastapi.responses import (
    HTMLResponse,
    RedirectResponse
)

from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from .database import get_db

from .schemas import (
    UserInput,
    FeedbackInput
)

from . import crud

from .ai.gemini_generator import (
    generate_workout_gemini
)

from .ai.gemini_flash_generator import (
    generate_nutrition_tip_with_flash
)

from .ai.updated_plan import (
    update_workout_plan
)


router = APIRouter()


BASE_DIR = Path(__file__).resolve().parent.parent


templates = Jinja2Templates(
    directory=str(
        BASE_DIR / "templates"
    )
)


# -------------------------------------------------
# HOME PAGE
# -------------------------------------------------

@router.get(
    "/",
    response_class=HTMLResponse
)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# -------------------------------------------------
# GENERATE WORKOUT
# -------------------------------------------------

@router.post(
    "/generate-workout",
    response_class=HTMLResponse
)
def generate_workout(

    request: Request,

    user_id: str = Form(...),

    username: str = Form(...),

    age: int = Form(...),

    weight: float = Form(...),

    goal: str = Form(...),

    intensity: str = Form(...),

    db: Session = Depends(get_db)

):

    try:

        user_data = UserInput(

            user_id=user_id.strip(),

            username=username.strip(),

            age=age,

            weight=weight,

            goal=goal.strip().lower(),

            intensity=intensity.strip().lower()

        )


        # Save user

        user = crud.save_user(
            db,
            user_data
        )


        # Generate workout using Gemini

        workout_plan = generate_workout_gemini(

            user_data.username,

            user_data.age,

            user_data.weight,

            user_data.goal,

            user_data.intensity

        )


        # Generate nutrition tip

        nutrition_tip = (
            generate_nutrition_tip_with_flash(

                user_data.goal,

                user_data.intensity

            )
        )


        # Save plan

        crud.save_plan(

            db,

            user,

            workout_plan,

            nutrition_tip

        )


        # Show result page

        return templates.TemplateResponse(

            request=request,

            name="result.html",

            context={
                "user": user,
                "plan": user.plan
            }

        )


    except Exception as exc:

        return templates.TemplateResponse(

            request=request,

            name="error.html",

            context={
                "error": str(exc)
            },

            status_code=400

        )


# -------------------------------------------------
# SUBMIT FEEDBACK
# -------------------------------------------------

@router.post(
    "/submit-feedback",
    response_class=HTMLResponse
)
def submit_feedback(

    request: Request,

    user_id: str = Form(...),

    feedback: str = Form(...),

    db: Session = Depends(get_db)

):

    try:

        feedback_data = FeedbackInput(

            user_id=user_id.strip(),

            feedback=feedback.strip()

        )


        # Find user

        user = crud.get_user(

            db,

            feedback_data.user_id

        )


        if user is None:

            raise ValueError(
                "User was not found."
            )


        if user.plan is None:

            raise ValueError(
                "Workout plan was not found."
            )


        # Get current plan

        current_plan = (

            user.plan.updated_plan

            or

            user.plan.original_plan

        )


        # Generate updated plan

        new_plan = update_workout_plan(

            current_plan,

            feedback_data.feedback,

            user.goal,

            user.intensity

        )


        # Save updated plan

        crud.update_plan(

            db,

            user,

            new_plan,

            feedback_data.feedback

        )


        # Show result page

        return templates.TemplateResponse(

            request=request,

            name="result.html",

            context={
                "user": user,
                "plan": user.plan
            }

        )


    except Exception as exc:

        return templates.TemplateResponse(

            request=request,

            name="error.html",

            context={
                "error": str(exc)
            },

            status_code=400

        )


# -------------------------------------------------
# VIEW ALL USERS
# -------------------------------------------------

@router.get(
    "/view-all-users",
    response_class=HTMLResponse
)
def view_all_users(

    request: Request,

    db: Session = Depends(get_db)

):

    users = crud.get_all_users(db)


    return templates.TemplateResponse(

        request=request,

        name="all_users.html",

        context={
            "users": users
        }

    )


# -------------------------------------------------
# DELETE USER
# -------------------------------------------------

@router.post(
    "/delete-user"
)
def delete_user(

    user_id: str = Form(...),

    db: Session = Depends(get_db)

):

    crud.delete_user(

        db,

        user_id

    )


    return RedirectResponse(

        url="/view-all-users",

        status_code=303
        
    )