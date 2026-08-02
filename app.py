from flask import Flask, request
from flask_migrate import Migrate

from config import Config
from models import db, Workout, Exercise, WorkoutExercise
from schemas import (
    WorkoutSchema,
    ExerciseSchema,
    WorkoutExerciseSchema
)

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)


workout_schema = WorkoutSchema()
exercise_schema = ExerciseSchema()
workout_exercise_schema = WorkoutExerciseSchema()


@app.route("/")
def home():
    return {
        "message": "Workout API is running"
    }


# =========================
# WORKOUTS
# =========================

@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return workout_schema.dump(workouts, many=True), 200


@app.route("/workouts/<int:workout_id>", methods=["GET"])
def get_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if not workout:
        return {
            "error": "Workout not found."
        }, 404

    return workout_schema.dump(workout), 200


@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json()

    if not data:
        return {
            "error": "Request body is required."
        }, 400

    try:
        validated_data = workout_schema.load(data)
    except Exception as e:
        return {
            "errors": e.messages
        }, 400

    existing_workout = Workout.query.filter_by(
        name=validated_data["name"]
    ).first()

    if existing_workout:
        return {
            "error": "Workout with this name already exists."
        }, 409

    workout = Workout(**validated_data)

    db.session.add(workout)
    db.session.commit()

    return workout_schema.dump(workout), 201


@app.route("/workouts/<int:workout_id>", methods=["PUT"])
def update_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if not workout:
        return {
            "error": "Workout not found."
        }, 404

    data = request.get_json()

    if not data:
        return {
            "error": "Request body is required."
        }, 400

    try:
        validated_data = workout_schema.load(data)
    except Exception as e:
        return {
            "errors": e.messages
        }, 400

    existing_workout = Workout.query.filter(
        Workout.name == validated_data["name"],
        Workout.id != workout_id
    ).first()

    if existing_workout:
        return {
            "error": "Workout with this name already exists."
        }, 409

    workout.name = validated_data["name"]
    workout.description = validated_data["description"]

    db.session.commit()

    return workout_schema.dump(workout), 200


@app.route("/workouts/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if not workout:
        return {
            "error": "Workout not found."
        }, 404

    db.session.delete(workout)
    db.session.commit()

    return {
        "message": "Workout deleted successfully."
    }, 200


# =========================
# EXERCISES
# =========================

@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    return exercise_schema.dump(exercises, many=True), 200


@app.route("/exercises/<int:exercise_id>", methods=["GET"])
def get_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if not exercise:
        return {
            "error": "Exercise not found."
        }, 404

    return exercise_schema.dump(exercise), 200


@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json()

    if not data:
        return {
            "error": "Request body is required."
        }, 400

    try:
        validated_data = exercise_schema.load(data)
    except Exception as e:
        return {
            "errors": e.messages
        }, 400

    existing_exercise = Exercise.query.filter_by(
        name=validated_data["name"]
    ).first()

    if existing_exercise:
        return {
            "error": "Exercise with this name already exists."
        }, 409

    exercise = Exercise(**validated_data)

    db.session.add(exercise)
    db.session.commit()

    return exercise_schema.dump(exercise), 201


@app.route("/exercises/<int:exercise_id>", methods=["PUT"])
def update_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if not exercise:
        return {
            "error": "Exercise not found."
        }, 404

    data = request.get_json()

    if not data:
        return {
            "error": "Request body is required."
        }, 400

    try:
        validated_data = exercise_schema.load(data)
    except Exception as e:
        return {
            "errors": e.messages
        }, 400

    existing_exercise = Exercise.query.filter(
        Exercise.name == validated_data["name"],
        Exercise.id != exercise_id
    ).first()

    if existing_exercise:
        return {
            "error": "Exercise with this name already exists."
        }, 409

    exercise.name = validated_data["name"]
    exercise.muscle_group = validated_data["muscle_group"]
    exercise.instructions = validated_data["instructions"]

    db.session.commit()

    return exercise_schema.dump(exercise), 200


@app.route("/exercises/<int:exercise_id>", methods=["DELETE"])
def delete_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if not exercise:
        return {
            "error": "Exercise not found."
        }, 404

    db.session.delete(exercise)
    db.session.commit()

    return {
        "message": "Exercise deleted successfully."
    }, 200


# =========================
# WORKOUT EXERCISES
# =========================

@app.route(
    "/workouts/<int:workout_id>/exercises",
    methods=["POST"]
)
def add_exercise_to_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if not workout:
        return {
            "error": "Workout not found."
        }, 404

    data = request.get_json()

    if not data:
        return {
            "error": "Request body is required."
        }, 400

    data["workout_id"] = workout_id

    try:
        validated_data = workout_exercise_schema.load(data)
    except Exception as e:
        return {
            "errors": e.messages
        }, 400

    exercise = db.session.get(
        Exercise,
        validated_data["exercise_id"]
    )

    if not exercise:
        return {
            "error": "Exercise not found."
        }, 404

    existing = WorkoutExercise.query.filter_by(
        workout_id=workout_id,
        exercise_id=validated_data["exercise_id"]
    ).first()

    if existing:
        return {
            "error": "Exercise is already assigned to this workout."
        }, 409

    workout_exercise = WorkoutExercise(
        workout_id=workout_id,
        exercise_id=validated_data["exercise_id"],
        sets=validated_data["sets"],
        reps=validated_data.get("reps"),
        duration=validated_data.get("duration")
    )

    db.session.add(workout_exercise)
    db.session.commit()

    return workout_exercise_schema.dump(workout_exercise), 201


@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>",
    methods=["DELETE"]
)
def delete_workout_exercise(workout_id, exercise_id):
    workout_exercise = WorkoutExercise.query.filter_by(
        workout_id=workout_id,
        exercise_id=exercise_id
    ).first()

    if not workout_exercise:
        return {
            "error": "Exercise not found in this workout."
        }, 404

    db.session.delete(workout_exercise)
    db.session.commit()

    return {
        "message": "Exercise removed from workout successfully."
    }, 200


if __name__ == "__main__":
    app.run(debug=True)