import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Prompt(BaseModel):
    name: str
    text: str
    version: int = 1
    tag: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    class Config:
        # Автоматическое приведение значений типов
        from_attributes = True

    @field_validator('name')
    def validate_name(cls, v):
        """Валидатор для имени, запрещающий пустые строки."""
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v

    def __repr__(self):
        return f"Prompt(name={self.name}, version={self.version}, created_at={self.created_at})"

    def to_str(self) -> str:
        """Пример дополнительного метода для вывода данных в строковом формате."""
        return f"{self.name} [{self.version}]: {self.text} (Tag: {self.tag or 'N/A'})"
