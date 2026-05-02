from fastapi import APIRouter, Depends, HTTPException,Path, Request
from typing import Annotated
from starlette import status
from sqlalchemy.orm import Session
##from models import Todo
from ..models import Todo
#import models
from ..models import Base
#from database import engine, sessionLocal
from ..database import engine, sessionLocal
from pydantic import BaseModel, Field
#from  routers import auth
from ..routers import auth
from .auth import get_current_user
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

templates=Jinja2Templates(directory="todoApp_mySQL/templates")
router=APIRouter(prefix="/todos",tags=["todos"])
#models.Base.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine)
router.include_router(auth.router)
user_dep=Annotated[dict,Depends(get_current_user)]

def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dep=Annotated[Session, Depends(get_db)]

def redirect_to_login():
    redirect_response= RedirectResponse(url="/auth/login-page",status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key='access_token')
    return redirect_response
### Pages ###
@router.get("/todo-page")
async def render_todo_page(request:Request,db:db_dep):
    try:
        user=await get_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()
        todos=db.query(Todo).filter(Todo.owner_id==user.get("id")).all()
        return templates.TemplateResponse("todo.html",{"request":request,"user":user,"todos":todos})
    except:
        return redirect_to_login()

@router.get("/add-todo-page")
async def render_add_todo_page(request: Request):
    try:
        user=await get_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()
        return templates.TemplateResponse("add-todo.html",{"request":request,"user":user})
    except:
        return redirect_to_login()

@router.get("/edit-todo-page/{todo_id}")
async def render_edit_todo_page(request:Request, todo_id:int, db:db_dep):
    try:
        user= await get_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()
        todo=db.query(Todo).filter(Todo.id==todo_id).first()
        return templates.TemplateResponse("edit-todo.html",{"request":request,"todo":todo,
                                                            "user":user})
    except:
        return redirect_to_login()
###End points ###
class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3)
    priority: int= Field(gt=0,lt=10)
    complete: bool

@router.get("/",status_code=status.HTTP_200_OK)
async def read_all(user:user_dep,db:db_dep):
    #return db.query(Todo).all()
    if(user is None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='You are not authorised')
    return db.query(Todo).filter(user.get('id')==Todo.owner_id).all()

@router.get("/todo/{todo_id}",status_code=status.HTTP_200_OK)
async def getTodoById(user:user_dep,db:db_dep,todo_id:int=Path(gt=0)):
    if(user is None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='You are not authorised')
    todo_model=db.query(Todo).filter(Todo.id==todo_id).filter(user.get('id')==Todo.owner_id).first()
    if todo_model is not None:
        return todo_model
    else:
        raise HTTPException(status_code=404,detail="Todo with this id not found.")
    

@router.post("/todo/",status_code=status.HTTP_201_CREATED)
async def create_todo(user:user_dep,db:db_dep, todo_request:TodoRequest):
    if(user is None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='You are not authorised')
    todo_model=Todo(**todo_request.model_dump(), owner_id=user.get('id'))
    db.add(todo_model)
    db.commit()

@router.put("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db:db_dep, user:user_dep,
                      todoReq:TodoRequest,
                      todo_id:int=Path(gt=0)
                      ):
    if(user is None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='You are not authorised')
    todo_model=db.query(Todo).filter(Todo.id==todo_id).filter(user.get('id')==Todo.owner_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail='Todo not found')
    todo_model.title= todoReq.title
    todo_model.description= todoReq.description
    todo_model.priority =todoReq.priority
    todo_model.complete =todoReq.complete
    db.add(todo_model)
    db.commit()


@router.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user:user_dep,db:db_dep,todo_id:int =Path(gt=0)):
    if(user is None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='You are not authorised')
    todo_model=db.query(Todo).filter(Todo.id==todo_id).filter(user.get('id')==Todo.owner_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo with this id not found")
    db.query(Todo).filter(Todo.id==todo_id).filter(user.get('id')==Todo.owner_id).delete()
    db.commit()
