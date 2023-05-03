from django.contrib.auth.validators import UnicodeUsernameValidator as _UsernameValidator
from django.core.validators import EmailValidator as _EmailValidator


username_validator = _UsernameValidator()
email_validator = _EmailValidator()
