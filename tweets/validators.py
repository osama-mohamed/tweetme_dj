from django.core.exceptions import ValidationError


def validate_content(value):
  if value == 'abc':
    raise ValidationError('Cannot be Empty from models validators')
  return value