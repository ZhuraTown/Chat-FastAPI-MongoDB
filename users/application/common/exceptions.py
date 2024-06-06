from dataclasses import dataclass

from fastapi.exceptions import ValidationException


class ApplicationException(Exception):
    @property
    def message(self) -> str:
        return "An application error occurred"


@dataclass
class ToClientException(ValidationException):
    errors: str