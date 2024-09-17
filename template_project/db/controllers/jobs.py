import uuid
from typing import Tuple

from sqlmodel import Session, and_, asc, col, func, select

from template_project.models.database import Job
from template_project.models.validation import JobBase


def create_job(job_in: JobBase, user_id: uuid.UUID, session: Session) -> Job:
    db_job = Job.model_validate(job_in, update={"user_id": user_id})
    session.add(db_job)
    session.flush()
    session.refresh(db_job)
    return db_job


def get_job(job_id: int, user_id: str, session: Session) -> Job | None:
    statement = select(Job).where(
        and_(col(Job.id) == job_id, col(Job.user_id) == user_id)
    )
    job = session.exec(statement).first()

    return job


def get_jobs(
    page: int,
    page_size: int,
    company_name: str | None,
    salary: float | None,
    user_id: str,
    session: Session,
) -> Tuple[int, list[Job]]:
    count_query = select(func.count()).select_from(Job)

    data_query = (
        select(Job)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .order_by(asc(Job.id))
    )

    filters = [col(Job.user_id) == user_id]

    if company_name:
        filters.append(col(Job.company_name).icontains(company_name, autoescape=True))

    if salary:
        filters.append(col(Job.salary) >= salary)

    if filters:
        count_query = count_query.where(and_(*filters))
        data_query = data_query.where(and_(*filters))

    count = session.exec(count_query).one()

    data = session.exec(data_query).all()

    return count, data


def delete_job(job_id: int, user_id: str, session: Session) -> int | None:
    db_job = session.get(Job, job_id)

    if not db_job:
        return None

    if db_job.user_id != uuid.UUID(user_id):
        return None

    session.delete(db_job)

    return job_id
