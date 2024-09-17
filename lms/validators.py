import re
from django.core.exceptions import ValidationError


YOUTUBE_REGEX = r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$'


def validate_youtube_url(value):
    if not re.match(YOUTUBE_REGEX, value):
        raise ValidationError("Допустимы только ссылки на youtube.com")
