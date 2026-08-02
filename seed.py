from app import app
from models import db, Workout, Exercise, WorkoutExercise


def seed_database():
    with app.app_context():
        db.session.query(WorkoutExercise).delete()
        db.session.query(Workout).delete()
        db.session.query(Exercise).delete()

        workout1 = Workout(
            name="Full Body Strength",
            description="A complete full body strength workout."
        )

        workout2 = Workout(
            name="Upper Body Day",
            description="A workout focused on upper body strength."
        )

        exercise1 = Exercise(
            name="Push Up",
            muscle_group="Chest",
            instructions="Keep your body straight and lower your chest toward the floor."
        )

        exercise2 = Exercise(
            name="Squat",
            muscle_group="Legs",
            instructions="Lower your hips while keeping your chest up and knees aligned."
        )

        exercise3 = Exercise(
            name="Pull Up",
            muscle_group="Back",
            instructions="Pull your body upward until your chin clears the bar."
        )

        db.session.add_all([
            workout1,
            workout2,
            exercise1,
            exercise2,
            exercise3
        ])

        db.session.commit()

        workout_exercise1 = WorkoutExercise(
            workout_id=workout1.id,
            exercise_id=exercise1.id,
            sets=3,
            reps=10
        )

        workout_exercise2 = WorkoutExercise(
            workout_id=workout1.id,
            exercise_id=exercise2.id,
            sets=3,
            reps=12
        )

        workout_exercise3 = WorkoutExercise(
            workout_id=workout2.id,
            exercise_id=exercise3.id,
            sets=4,
            reps=8
        )

        db.session.add_all([
            workout_exercise1,
            workout_exercise2,
            workout_exercise3
        ])

        db.session.commit()

        print("Database seeded successfully!")


if __name__ == "__main__":
    seed_database()