from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from deps import get_current_user
from app.db.database import get_db
from app.db.models import User
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.repositories import task_repo

router = APIRouter(
    prefix="api/v1/tasks",
    tags=["Tasks"]
)

@router.get("", response_model=List[TaskResponse])
def read_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return task_repo.get_tasks_by_user(db=db, user_id=current_user.id)

@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return task_repo.create_task(db=db, task=task, user_id=current_user.id)

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_task = task_repo.get_task_by_id_and_user(db=db, task_id=task_id, user_id=current_user.id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_repo.update_task(db=db, db_task=db_task, task_update=task_update)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_task = task_repo.get_task_by_id_and_user(db=db, task_id=task_id, user_id=current_user.id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    task_repo.delete_task(db=db, db_task=db_task)
    return {"message": "Task deleted successfully"}