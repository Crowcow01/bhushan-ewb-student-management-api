from sqlalchemy import CheckConstraint, Column, Integer, String

from app.database import Base


class Student(Base):
    __tablename__ = "students"

    __table_args__ = (
        CheckConstraint(
            "age IS NULL OR (age >= 0 AND age <= 120)",
            name="check_student_age",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    email = Column(String(254), unique=True, nullable=False, index=True)
    age = Column(Integer, nullable=True)
    course = Column(String(100), nullable=False)