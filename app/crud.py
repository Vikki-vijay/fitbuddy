from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import User, Plan
from .schemas import UserInput


def get_user(
    db: Session,
    user_id: str
):

    return db.scalar(
        select(User).where(
            User.user_id == user_id
        )
    )


def save_user(
    db: Session,
    data: UserInput
):

    user = get_user(
        db,
        data.user_id
    )

    if user is None:

        user = User(
            user_id=data.user_id,
            username=data.username,
            age=data.age,
            weight=data.weight,
            goal=data.goal,
            intensity=data.intensity
        )

        db.add(user)

    else:

        user.username = data.username
        user.age = data.age
        user.weight = data.weight
        user.goal = data.goal
        user.intensity = data.intensity

    db.commit()

    db.refresh(user)

    return user


def save_plan(
    db: Session,
    user: User,
    original_plan: str,
    nutrition_tip: str
):

    plan = user.plan

    if plan is None:

        plan = Plan(
            user_id=user.id,
            original_plan=original_plan,
            nutrition_tip=nutrition_tip
        )

        db.add(plan)

    else:

        plan.original_plan = original_plan
        plan.nutrition_tip = nutrition_tip
        plan.updated_plan = None
        plan.feedback = None
        plan.updated_at = None

    db.commit()

    db.refresh(user)

    return plan


def update_plan(
    db: Session,
    user: User,
    updated_plan: str,
    feedback: str
):

    if user.plan is None:

        raise ValueError(
            "Workout plan does not exist."
        )

    user.plan.updated_plan = updated_plan

    user.plan.feedback = feedback

    user.plan.updated_at = datetime.utcnow()

    db.commit()

    db.refresh(user)

    return user.plan


def get_all_users(
    db: Session
):

    return db.scalars(
        select(User).order_by(
            User.created_at.desc()
        )
    ).all()


def delete_user(
    db: Session,
    user_id: str
):

    user = get_user(
        db,
        user_id
    )

    if user:

        db.delete(user)

        db.commit()