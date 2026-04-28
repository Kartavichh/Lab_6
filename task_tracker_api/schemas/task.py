import re
import html
from typing import Optional, Literal, Annotated  # ← Annotated обязателен!
from datetime import datetime, timezone
from pydantic import BaseModel, Field, field_validator, BeforeValidator

def sanitize_html(value: str | None) -> str | None:
    if value is None:
        return None
    return re.sub(r'<[^>]+>', '', html.unescape(value)).strip()

# Создаём переиспользуемый тип для "очищенных строк"
SanitizedStr = Annotated[str, BeforeValidator(sanitize_html)]
OptionalSanitizedStr = Annotated[Optional[str], BeforeValidator(sanitize_html)]

class TaskCreate(BaseModel):
    title: SanitizedStr = Field(..., min_length=3, max_length=150)
    description: OptionalSanitizedStr = Field(None, max_length=1000)
    priority: Literal["low", "medium", "high"] = "medium"
    due_date: datetime
    status: Literal["todo", "in_progress", "done"] = "todo"
    assigned_email: SanitizedStr = Field(..., min_length=5, max_length=100)

    @field_validator('due_date')
    @classmethod
    def validate_future_date(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            if v <= datetime.now():
                raise ValueError('Дедлайн должен быть в будущем')
        else:
            if v <= datetime.now(timezone.utc):
                raise ValueError('Дедлайн должен быть в будущем')
        return v

class TaskUpdate(BaseModel):
    title: Optional[SanitizedStr] = Field(None, min_length=3, max_length=150)
    description: OptionalSanitizedStr = Field(None, max_length=1000)
    priority: Optional[Literal["low", "medium", "high"]] = None
    due_date: Optional[datetime] = None
    status: Optional[Literal["todo", "in_progress", "done"]] = None
    assigned_email: Optional[SanitizedStr] = Field(None, min_length=5, max_length=100)

    @field_validator('due_date')
    @classmethod
    def validate_future_date(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v is None:
            return v
        if v.tzinfo is None:
            if v <= datetime.now():
                raise ValueError('Дедлайн должен быть в будущем')
        else:
            if v <= datetime.now(timezone.utc):
                raise ValueError('Дедлайн должен быть в будущем')
        return v

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: str
    status: str
    due_date: datetime
    assigned_email: str
    created_at: datetime
    updated_at: Optional[datetime] = None