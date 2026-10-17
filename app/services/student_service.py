from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Student
from app.schemas import StudentCreate, StudentUpdate


def create_student(db: Session, student_data: StudentCreate) -> Student:
    student = Student(**student_data.model_dump())
    db.add(student)

    try:
        db.commit()
        db.refresh(student)
    except IntegrityError:
        db.rollback()
        raise ValueError("A student with this email already exists.")

    return student


def get_students(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: str | None = None,
) -> list[Student]:
    query = select(Student)

    if search:
        query = query.where(Student.name.ilike(f"%{search}%"))

    query = query.order_by(Student.id).offset(skip).limit(limit)
    return list(db.scalars(query).all())


def get_student(db: Session, student_id: int) -> Student | None:
    return db.get(Student, student_id)


def update_student(
    db: Session,
    student: Student,
    student_data: StudentUpdate,
) -> Student:
    updates = student_data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(student, field, value)

    try:
        db.commit()
        db.refresh(student)
    except IntegrityError:
        db.rollback()
        raise ValueError("A student with this email already exists.")

    return student


def delete_student(db: Session, student: Student) -> None:
    db.delete(student)
    db.commit()