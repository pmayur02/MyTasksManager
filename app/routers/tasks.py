from fastapi import APIRouter
from app.schemas.todo import task,taskResponse,taskUpdate
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.database.db import get_db
from app.models.models import Task,User
from app.utilities.authentication import get_current_user
from sqlalchemy.orm import Session


taskRouter = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


@taskRouter.post("/add-tasks", response_model=taskResponse)
def create(task: task, db: Session = Depends(get_db), currentUser: User = Depends(get_current_user)):
    try:
        newTask = Task(title=task.title,description=task.description,user_id=currentUser.id)
        db.add(newTask)
        db.commit()
        db.refresh(newTask)
        return newTask

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create task: {str(e)}"
        )


@taskRouter.get("/", response_model=List[taskResponse])
def getAllTasks(db: Session = Depends(get_db), currentUser: User = Depends(get_current_user)):
    try:
        tasks = db.query(Task).filter(Task.user_id == currentUser.id, Task.status != "complete").all()

        if len(tasks) == 0:
            return []

        return tasks

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch tasks: {str(e)}"
        )


@taskRouter.get('/{id}', response_model=taskResponse)
def getTask(id: int, db: Session = Depends(get_db), currentUser: User = Depends(get_current_user)):
    try:
        task = db.query(Task).filter(
            Task.id == id,
            Task.user_id == currentUser.id
        ).first()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No tasks found"
            )

        return task

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch task: {str(e)}"
        )


@taskRouter.put('/update-task/{id}', response_model=taskResponse)
def updateTask(id: int, taskupdate: taskUpdate, db: Session = Depends(get_db), currentUser: User = Depends(get_current_user)):
    try:
        task = db.query(Task).filter(
            Task.id == id,
            Task.status != "complete",
            Task.user_id == currentUser.id
        ).first()

        if not task:
            raise HTTPException(
                status_code=404,
                detail="No task found for this id"
            )

        update_data = taskupdate.model_dump(exclude_unset=True)

        if "status" in update_data and update_data['status'] is not None:
            update_data['status'] = update_data['status'].value

        for key, value in update_data.items():
            setattr(task, key, value)

        db.commit()
        db.refresh(task)

        return task

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update task: {str(e)}"
        )


@taskRouter.delete('/delete-task/{id}')
def deleteTask(id: int, db: Session = Depends(get_db), currentUser: User = Depends(get_current_user)):
    try:
        task = db.query(Task).filter(
            Task.id == id,
            Task.status != "complete",
            Task.user_id == currentUser.id
        ).first()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No task found for this id"
            )

        task.status = "complete"
        db.commit()
        db.refresh(task)

        return {
            "status": status.HTTP_204_NO_CONTENT,
            "message": "task deleted successfully"
        }

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete task: {str(e)}"
        )

