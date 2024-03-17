from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Todo, TodoCreate, TodoOut, TodosOut, TodoUpdate, Message

router = APIRouter()

@router.get("/", response_model=TodosOut)
def read_todos(session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve todos.
    """
    
    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Todo)
        count = session.exec(count_statement).one()
        statement = select(Todo).offset(skip).limit(limit)
        todos = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Todo)
            .where(Todo.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Todo)
            .where(Todo.owner_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )
        items = session.exec(statement).all()
        
    return TodosOut(todos=todos, count=count)

@router.get("/{id}", response_model=TodoOut)
def read_todo(session: SessionDep, current_user:CurrentUser, id: int) -> Any:
    """
    Retrieve todo by ID.
    """
    todo = session.get(Todo, id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if not current_user.is_superuser and todo.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return todo

@router.post("/", response_model=TodoOut)
def create_todo(*, session: SessionDep, current_user: CurrentUser, todo_in: TodoCreate) -> Any:
    """
    Create new todo.
    """
    todo = Todo.model_validate(todo_in, update={"owner_id": current_user.id})
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@router.put("/{id}", response_model=TodoOut)
def update_todo(*, session: SessionDep, current_user: CurrentUser, id: int, todo_in: TodoUpdate) -> Any:
    """
    Update a todo.
    """
    todo = session.get(Todo, id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if not current_user.is_superuser and todo.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = todo_in.dict(exclude_unset=True)
    todo.sqlmodel_update(update_dict)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@router.delete("/{id}")
def delete_todo(*, session: SessionDep, current_user: CurrentUser, id: int) -> Message:
    """
    Delete a todo.
    """
    todo = session.get(Todo, id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if not current_user.is_superuser and todo.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(todo)
    session.commit()
    return Message(message="Todo deleted successfully")