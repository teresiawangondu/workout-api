# Workout API

## Project Description

Workout API is a Flask backend application for managing workouts and reusable exercises. It uses Flask, SQLAlchemy, Flask-Migrate, and Marshmallow to provide a RESTful API for creating, viewing, and deleting workouts and exercises, as well as adding exercises to workouts.

The application demonstrates database relationships, serialization, model validation, schema validation, database constraints, migrations, and seed data.

## Technologies

* Python
* Flask 2.2.2
* Flask-SQLAlchemy 3.0.3
* Flask-Migrate 3.1.0
* Marshmallow 3.20.1
* SQLite
* Pipenv

## Installation

Clone the repository and navigate into the project directory:

```bash
cd workout-api
```

Install the project dependencies:

```bash
pipenv install
```

Enter the Pipenv virtual environment:

```bash
pipenv shell
```

## Database Setup

Initialize the Flask-Migrate migration directory if it has not already been created:

```bash
flask --app app db init
```

Create a migration:

```bash
flask --app app db migrate -m "create workout tables"
```

Apply the migration:

```bash
flask --app app db upgrade
```

Seed the database with example workouts and exercises:

```bash
python seed.py
```

## Running the Application

Start the Flask development server:

```bash
python app.py
```

The API will be available at:

```text
http://127.0.0.1:5000
```

## API Endpoints

### Workouts

#### GET /workouts

Returns all workouts and their associated exercises.

#### GET /workouts/<workout_id>

Returns a single workout by ID, including its associated exercises.

#### POST /workouts

Creates a new workout.

Example request body:

```json
{
    "name": "Morning Power",
    "description": "A balanced morning strength workout."
}
```

#### DELETE /workouts/<workout_id>

Deletes a workout by ID.

---

### Exercises

#### GET /exercises

Returns all exercises.

#### GET /exercises/<exercise_id>

Returns a single exercise by ID.

#### POST /exercises

Creates a new exercise.

Example request body:

```json
{
    "name": "Mountain Climbers",
    "muscle_group": "Core",
    "instructions": "Drive your knees toward your chest quickly while maintaining a strong plank position."
}
```

#### DELETE /exercises/<exercise_id>

Deletes an exercise by ID.

---

### Workout Exercises

#### POST /workouts/<workout_id>/exercises

Adds an existing exercise to a workout.

Example request body:

```json
{
    "exercise_id": 4,
    "sets": 3,
    "reps": 15
}
```

The API supports either repetitions or duration depending on the workout exercise configuration.

## Validation

The application includes validation at multiple levels.

### Table Constraints

Database constraints are used to enforce:

* Minimum workout name length
* Minimum workout description length
* Minimum exercise name length
* Minimum muscle group length
* Positive number of sets
* Positive number of reps when provided
* Positive duration when provided
* Unique workout/exercise combinations

### Model Validations

SQLAlchemy model validators ensure that:

* Workout names meet minimum length requirements
* Workout descriptions meet minimum length requirements
* Exercise names meet minimum length requirements
* Muscle groups meet minimum length requirements
* Sets are greater than zero
* Reps are greater than zero when provided
* Duration is greater than zero when provided

### Schema Validations

Marshmallow schemas validate incoming request data before it reaches the database.

Examples include:

* Required fields
* String length requirements
* Integer validation
* Positive values for sets and reps
* Valid workout and exercise relationships

## Database Relationships

The application contains three database models:

* `Workout`
* `Exercise`
* `WorkoutExercise`

A workout can contain multiple exercises, and an exercise can be reused across multiple workouts.

`WorkoutExercise` acts as the association model between workouts and exercises and stores workout-specific information such as sets, reps, and duration.

## Seed Data

The `seed.py` file creates example data for:

* Workouts
* Exercises
* Workout-exercise relationships

Run:

```bash
python seed.py
```

to populate the database.

## Testing

The API can be tested using Postman or another API client.

Example base URL:

```text
http://127.0.0.1:5000
```

Test successful requests as well as validation errors, duplicate records, missing records, and invalid IDs.

## Project Structure

```text
workout-api/
│
├── app.py
├── models.py
├── schemas.py
├── seed.py
├── config.py
├── Pipfile
├── Pipfile.lock
├── README.md
├── migrations/
├── instance/
└── .gitignore
```
