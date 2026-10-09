from pydantic import BaseModel, Field, field_validator

from app.shared.validators.identifier import IdentifierType, detect_identifier_type, normalize_identifier


class CreateCheckRequest(BaseModel):
    query: str = Field(..., min_length=10, max_length=32, description="ИНН или ОГРН")

    @field_validator("query")
    @classmethod
    def validate_query(cls, value: str) -> str:
        normalized = normalize_identifier(value)
        if detect_identifier_type(normalized) == IdentifierType.UNKNOWN:
            raise ValueError("Ожидается ИНН (10/12 цифр) или ОГРН/ОГРНИП (13/15 цифр)")
        return normalized
