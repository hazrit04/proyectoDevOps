from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal
from app.routers.auth import get_current_user
from datetime import datetime, timezone

router = APIRouter()

# Importar la base de datos

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Obtener tasks

@router.get("/tasks", response_model=list[schemas.TaskOut])
def get_tasks(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Task).filter(models.Task.user_id == current_user.user_id).all()

# Crear nuevo tasks

@router.post("/tasks", response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    new_task = models.Task(
        user_id=current_user.user_id,
        title=task.title,
        description=task.description,
        state=task.state,
        creation_date=datetime.now(timezone.utc),
        due_date=task.due_date
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    history = models.TaskHistory(
        task_id=new_task.task_id,
        last_state=None,
        actual_state=new_task.state,
        change_date=datetime.now(timezone.utc)
    )
    db.add(history)
    db.commit()

    return new_task

# Actualizar historial de task

@router.put("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, updated_task: schemas.TaskUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    task = db.query(models.Task).filter(models.Task.task_id == task_id, models.Task.user_id == current_user.user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    last_state = task.state
    task.title = updated_task.title
    task.description = updated_task.description
    task.state = updated_task.state
    task.due_date = updated_task.due_date
    db.commit()

    history = db.query(models.TaskHistory).filter(models.TaskHistory.task_id == task.task_id).first()
    history.last_state = last_state
    history.actual_state = task.state
    history.change_date = datetime.now(timezone.utc)
    db.commit()

    return task

# Eliminar task

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    task = db.query(models.Task).filter(models.Task.task_id == task_id, models.Task.user_id == current_user.user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    history = db.query(models.TaskHistory).filter(models.TaskHistory.task_id == task.task_id).first()
    if history:
        db.delete(history)
    db.delete(task)
    db.commit()
    return {"detail": "Tarea eliminada"}
