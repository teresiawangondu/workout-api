# Marshmallow schemas
from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)

    name = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=100)
    )

    muscle_group = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=50)
    )

    instructions = fields.Str(
        required=True,
        validate=validate.Length(min=5, max=500)
    )


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)

    workout_id = fields.Int(
        required=True,
        validate=validate.Range(min=1)
    )

    exercise_id = fields.Int(
        required=True,
        validate=validate.Range(min=1)
    )

    sets = fields.Int(
        required=True,
        validate=validate.Range(min=1)
    )

    reps = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1)
    )

    duration = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1)
    )

    @validates_schema
    def validate_reps_or_duration(self, data, **kwargs):
        reps = data.get("reps")
        duration = data.get("duration")

        if reps is None and duration is None:
            raise ValidationError(
                "Provide either reps or duration."
            )


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)

    name = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=100)
    )

    description = fields.Str(
        required=True,
        validate=validate.Length(min=5, max=255)
    )

    workout_exercises = fields.Nested(
        WorkoutExerciseSchema,
        many=True,
        dump_only=True
    )