from sqlalchemy.orm import Session

from app.db.models import Task
from app.schemas.task import TaskCreate, TaskUpdate


def get_tasks_by_user(db: Session, user_id: int):
    return db.query(Task).filter(Task.owner_id == user_id).all()

def get_task_by_id_and_user(db: Session, task_id: int, user_id: int):
    return db.query(Task).filter(Task.id == task_id, Task.owner_id == user_id).first()

def create_task(db: Session, task: TaskCreate, user_id: int):
    db_task = Task(**task.model_dump(), owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, db_task: Task, task_update: TaskUpdate):
    # model_dump(exclude_unset=True) ensures we only update fields Android actually sent
    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, db_task: Task):
    db.delete(db_task)
    db.commit()