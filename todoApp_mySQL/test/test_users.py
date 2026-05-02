from .utils import *
from ..routers.users import get_current_user,get_db
from fastapi import status

app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_current_user]=override_get_current_user

def test_return_user(test_user):
    res=client.get("/users")
    assert res.status_code==status.HTTP_200_OK
    assert res.json()[0]['username']=="User1"
    assert res.json()[0]['email']=="user1@gmail.com"
    assert res.json()[0]['first_name']=="User"
    assert res.json()[0]['last_name']=="1"
    assert res.json()[0]['phone_number']=="999-(999)-(9999)"
    assert res.json()[0]['role']=="admin"

def test_change_password(test_user):
    res=client.put("/users/password",json={"password":"test1234","new_password":"changed_password"})
    assert res.status_code==status.HTTP_204_NO_CONTENT

def test_change_password_invalid_current_password(test_user):
    res=client.put("/users/password",json={"password":"test1234!","new_password":"changed_password"})
    assert res.status_code==status.HTTP_401_UNAUTHORIZED

def test_change_phone_number(test_user):
    res=client.put("/users/phonenumber/?userPhNo=333333")
    assert res.status_code==status.HTTP_204_NO_CONTENT
    
