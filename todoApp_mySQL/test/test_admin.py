from .utils import *
from ..routers.admin import get_current_user, get_db

app.dependency_overrides[get_current_user]=override_get_current_user
app.dependency_overrides[get_db]=override_get_db

def test_admin_read_all_authenticated(test_todo):
    res=client.get('/admin/todo')
    assert res.status_code==200
    assert res.json()==[{
        "title":"Learn Fast API","description":"3 months","priority":5,"complete":False,
              "owner_id":1,"id":1
    }]

def test_admin_delete_todo(test_todo):
    res=client.delete("/admin/todo/1")
    assert res.status_code==204
    db=TestingSessionLocal()
    model=db.query(Todo).filter(Todo.id==1).first()
    assert model is None

def test_admin_delete_todo_not_found(test_todo):
    res=client.delete("/admin/todo/999")
    assert res.status_code==404
    assert res.json() =={'detail':'Todo with this id not found'}