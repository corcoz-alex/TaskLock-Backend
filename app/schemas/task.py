from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    is_completed: bool = False

# Sent by Android to create a task
class TaskCreate(TaskBase):
    pass

# Sent by Android to update a task
class TaskUpdate(TaskBase):
    pass

# Sent by FastAPI to Android when returning a task
class TaskResponse(TaskBase):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)