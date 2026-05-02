from sqlalchemy import text

from ..main import app
from ..routers.todo import get_current_user,get_db

from fastapi.testclient import TestClient
from fastapi import status

import pytest
from ..models import Todo
from .utils import *

app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_current_user]=override_get_current_user

client=TestClient(app)
@pytest.fixture
def test_todo():
    todo=Todo(title="Learn Fast API",description="3 months",priority=5,complete=False,
              owner_id=1)
    db=TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield db
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()
def test_read_all_authenticated(test_todo):
    res=client.get("/todos")
    print(res.json())
    assert res.status_code==status.HTTP_200_OK
    assert res.json()==[{'title':"Learn Fast API",'description':"3 months",'priority':5,
                         'complete':False,"owner_id":1,'id':1}]

def test_read_one_authenticated(test_todo):
    res=client.get("/todos/todo/1")
    print(res.json())
    assert res.status_code==status.HTTP_200_OK
    assert res.json()=={'title':"Learn Fast API",'description':"3 months",'priority':5,
                         'complete':False,"owner_id":1,'id':1}
    
def test_read_one_authenticated_not_found(test_todo):
    res=client.get("/todos/todo/999")
    print(res.json())
    assert res.status_code==status.HTTP_404_NOT_FOUND
    assert res.json()== {'detail': 'Todo with this id not found.'}

def test_create_todo(test_todo):
    request_data={'title':'New Todo','description':'New Desc','priority':4,
                  'complete':False}
    res=client.post("/todos/todo",json=request_data)
    assert res.status_code==status.HTTP_201_CREATED
    db=TestingSessionLocal()
    model=db.query(Todo).filter(Todo.id==2).first()
    assert model.title==request_data.get('title')
    assert model.description==request_data.get('description')
    assert model.priority==request_data.get('priority')
    assert model.complete ==request_data.get('complete')

def test_update_todo(test_todo):
    request_data={'title':'Updated Todo','description':'Updated Desc','priority':5,
                  'complete':True}
    res=client.put('/todos/todo/1',json=request_data)
    assert res.status_code==204
    db=TestingSessionLocal()
    model=db.query(Todo).filter(Todo.id==1).first()
    assert model.title==request_data.get('title')
    assert model.description==request_data.get('description')
    assert model.priority==request_data.get('priority')
    assert model.complete==request_data.get('complete')

def test_update_todo_not_found(test_todo):
    request_data={'title':'Updated Todo','description':'Updated Desc','priority':5,
                  'complete':True}
    res=client.put('/todos/todo/999',json=request_data)
    assert res.status_code==404
    assert res.json()=={'detail':'Todo not found'}

def test_delete_todo(test_todo):
    res=client.delete('/todos/todo/1')
    assert res.status_code==204
    db=TestingSessionLocal()
    model = db.query(Todo).filter(Todo.id==1).first()
    assert model is None

def test_delete_todo_not_found(test_todo):
    res=client.delete('/todos/todo/999')
    assert res.status_code==404
    assert res.json()=={'detail':'Todo with this id not found'}