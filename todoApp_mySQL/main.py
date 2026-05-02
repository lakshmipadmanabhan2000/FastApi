from fastapi import FastAPI, Request

#import models
from .models import Base
#from database import engine
from .database import engine
#from routers import auth,todo,admin,users
from  .routers import auth,todo,admin,users

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette import status
app=FastAPI()
#models.Base.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine)

template=Jinja2Templates(directory="todoApp_mySQL/templates")
app.mount("/static",StaticFiles(directory="todoApp_mySQL/static"),name="static")
@app.get("/")
def test(request: Request):
    #return template.TemplateResponse("home.html",{"request":request})
    return RedirectResponse(url="/todos/todo-page",status_code=status.HTTP_302_FOUND)

@app.get("/healthy")
def health_check():
    return {'status':'Healthy'}
app.include_router(auth.router)
app.include_router(todo.router)
app.include_router(admin.router)
app.include_router(users.router)

