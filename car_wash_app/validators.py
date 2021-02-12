from django.core.exceptions import ValidationError


def validate_licence_plate(value):
    if len(value) != 7 or len(value) != 6:
        raise ValidationError('ნომერი უნდა იყოს 7 ან 6 ნიშნა')