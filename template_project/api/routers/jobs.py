from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlmodel import Session

from template_project.api.auth import verify_jwt_token
from template_project.api.dependencies import get_session_by_user
from template_project.db.controllers import jobs
from template_project.models.validation import (
    JobBase,
    JobResponse,
    JobsRequest,
    JobsResponse,
    PaginationRequest,
)

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
)


@router.post("", response_model=JobResponse)
async def create_job(
    body: JobBase,
    session: Session = Depends(get_session_by_user),
    payload: dict = Depends(verify_jwt_token),
) -> Any:
    job = jobs.create_job(session=session, job_in=body, user_id=payload["sub"])
    return job


@router.get("/{job_id}", response_model=JobResponse)
async def read_job(
    job_id: int = Path(),
    session: Session = Depends(get_session_by_user),
    payload: dict = Depends(verify_jwt_token),
) -> Any:
    job = jobs.get_job(session=session, job_id=job_id, user_id=payload["sub"])

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found"
        )

    return job


@router.get("", response_model=JobsResponse)
async def read_jobs(
    pagination: Annotated[PaginationRequest, Depends()],
    params: Annotated[JobsRequest, Depends()],
    session: Session = Depends(get_session_by_user),
    payload: dict = Depends(verify_jwt_token),
) -> Any:
    count, data = jobs.get_jobs(
        session=session,
        page=pagination.page,
        page_size=pagination.page_size,
        company_name=params.company_name,
        salary=params.salary,
        user_id=payload["sub"],
    )

    return JobsResponse(data=data, total=count)


@router.delete("/{job_id}")
async def delete_job(
    job_id: int,
    session: Session = Depends(get_session_by_user),
    payload: dict = Depends(verify_jwt_token),
) -> dict:
    deleted_job_id = jobs.delete_job(
        session=session, job_id=job_id, user_id=payload["sub"]
    )

    if not deleted_job_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Could not delete the job"
        )

    return {"job_id": deleted_job_id}
