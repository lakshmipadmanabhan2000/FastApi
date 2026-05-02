from .utils import *
from ..routers.auth import get_db, authenticate_user,create_access_token,get_current_user
from jose import jwt
from datetime import timedelta
import pytest
from fastapi import HTTPException
app.dependency_overrides[get_db]=override_get_db
SECRET_KEY='d26dae912bab8f6c709b2d104747d834d4d11f59732c4a2e44add3c70d5b311f'
ALGORITHM='HS256'
def test_authenticate_user(test_user):
    db=TestingSessionLocal()
    authenticated_user=authenticate_user(db,test_user.username,'test1234')
    assert authenticated_user is not None
    assert authenticated_user.username==test_user.username

    #non-existent user
    invalid_user=authenticate_user(db,'TestUser1','test1234')
    assert invalid_user is False

    #wrong password
    invalid_user=authenticate_user(db,'TestUser','test1234@')
    assert invalid_user is False

def test_create_access_token():
    username='Test123'
    id=123
    role="admin"
    timedelay=timedelta(days=1)
    token=create_access_token(username,id,role,timedelay)
    decodedToken=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    assert decodedToken['sub']==username
    assert decodedToken['role']==role
    assert decodedToken['id']==id

@pytest.mark.asyncio
async def test_get_current_user():
    encode={'sub':'test123','id':1,'role':"admin"}
    token=jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)
    user= await get_current_user(token=token)
    assert user=={'username':'test123','id':1,'role':"admin"}

@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode={'role':'user'}
    token=jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)
    with pytest.raises(HTTPException) as exec:
        await get_current_user(token)
    assert exec.value.status_code==401
    assert exec.value.detail=='Could not validate credentials'