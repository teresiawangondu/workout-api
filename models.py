from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint


db = SQLAlchemy()


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    description = db.Column(
        db.String(255),
        nullable=False
    )

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint(
            "length(trim(name)) >= 3",
            name="workout_name_min_length"
        ),
        CheckConstraint(
            "length(trim(description)) >= 5",
            name="workout_description_min_length"
        ),
    )

    @validates("name")
    def validate_name(self, key, value):
        if not value or len(value.strip()) < 3:
            raise ValueError(
                "Workout name must be at least 3 characters."
            )
        return value.strip()

    @validates("description")
    def validate_description(self, key, value):
        if not value or len(value.strip()) < 5:
            raise ValueError(
                "Workout description must be at least 5 characters."
            )
        return value.strip()


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    muscle_group = db.Column(
        db.String(50),
        nullable=False
    )

    instructions = db.Column(
        db.String(500),
        nullable=False
    )

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint(
            "length(trim(name)) >= 3",
            name="exercise_name_min_length"
        ),
        CheckConstraint(
            "length(trim(muscle_group)) >= 3",
            name="exercise_muscle_group_min_length"
        ),
    )

    @validates("name")
    def validate_name(self, key, value):
        if not value or len(value.strip()) < 3:
            raise ValueError(
                "Exercise name must be at least 3 characters."
            )
        return value.strip()

    @validates("muscle_group")
    def validate_muscle_group(self, key, value):
        if not value or len(value.strip()) < 3:
            raise ValueError(
                "Muscle group must be at least 3 characters."
            )
        return value.strip()


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)

    workout_id = db.Column(
        db.Integer,
        db.ForeignKey("workouts.id"),
        nullable=False
    )

    exercise_id = db.Column(
        db.Integer,
        db.ForeignKey("exercises.id"),
        nullable=False
    )

    sets = db.Column(
        db.Integer,
        nullable=False
    )

    reps = db.Column(
        db.Integer,
        nullable=True
    )

    duration = db.Column(
        db.Integer,
        nullable=True
    )

    workout = db.relationship(
        "Workout",
        back_populates="workout_exercises"
    )

    exercise = db.relationship(
        "Exercise",
        back_populates="workout_exercises"
    )

    __table_args__ = (
        CheckConstraint(
            "sets > 0",
            name="sets_positive"
        ),
        CheckConstraint(
            "reps IS NULL OR reps > 0",
            name="reps_positive"
        ),
        CheckConstraint(
            "duration IS NULL OR duration > 0",
            name="duration_positive"
        ),
        db.UniqueConstraint(
            "workout_id",
            "exercise_id",
            name="unique_workout_exercise"
        ),
    )

    @validates("sets")
    def validate_sets(self, key, value):
        if value is None or value <= 0:
            raise ValueError(
                "Sets must be greater than 0."
            )
        return value

    @validates("reps")
    def validate_reps(self, key, value):
        if value is not None and value <= 0:
            raise ValueError(
                "Reps must be greater than 0."
            )
        return value

    @validates("duration")
    def validate_duration(self, key, value):
        if value is not None and value <= 0:
            raise ValueError(
                "Duration must be greater than 0."
            )
        return value