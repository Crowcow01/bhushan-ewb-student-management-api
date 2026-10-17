from pydantic import BaseModel, ConfigDict, EmailStr, Field


class StudentBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int | None = Field(default=None, ge=0, le=120)
    course: str = Field(min_length=1, max_length=100)


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
    age: int | None = Field(default=None, ge=0, le=120)
    course: str | None = Field(default=None, min_length=1, max_length=100)


class StudentResponse(StudentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class AIQuestion(BaseModel):
    question: str = Field(min_length=1, max_length=500)


class AIAnswer(BaseModel):
    question: str
    answer: str
