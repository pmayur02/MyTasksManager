from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class taskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "complete"

class task(BaseModel):
    title: str = Field(..., max_length=50, min_length=4)
    description: str = Field(..., max_length=200, min_length=5)
    status: taskStatus = taskStatus.pending

class taskResponse(BaseModel):
    id:int
    title: str
    description: str
    status: str

class taskUpdate(BaseModel):
    title:Optional[str] = None
    description:Optional[str] = None
    status: Optional[taskStatus] = None