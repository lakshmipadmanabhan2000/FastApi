from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext

from database import sessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt,JWTError
from datetime import timedelta,datetime,timezone
router=APIRouter(prefix='/auth',tags=['authorization'])
bcrypt_context=CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer=OAuth2PasswordBearer(tokenUrl='auth/token')

SECRET_KEY='d26dae912bab8f6c709b2d104747d834d4d11f59732c4a2e44add3c70d5b311f'
ALGORITHM='HS256'
def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dep= Annotated[Session, Depends(get_db)]
class UserRequest(BaseModel):
    email: str
    username: str
    password: str
    first_name: str
    last_name: str
    role: str

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dep,user_req:UserRequest):
    userReq_model=Users(
        email= user_req.email,
        first_name= user_req.first_name,
        last_name= user_req.last_name,
        role= user_req.role,
        username= user_req.username,
        hashed_password= bcrypt_context.hash(user_req.password),
        is_Active=True
    )
    db.add(userReq_model)
    db.commit()
def authenticate_user(db,username:str,password:str):
    user_model=db.query(Users).filter(Users.username==username).first()
    if not user_model:
        return False
    if not bcrypt_context.verify(password,user_model.hashed_password):
        return False
    return user_model
class Token(BaseModel):
    access_token:str
    token_type:str
def create_access_token(username:str,userid:int,userrole:str,timedelay:timedelta):
    encoding={'sub':username,'id':userid,'role':userrole}
    exp_time=timedelay+datetime.now(timezone.utc)
    encoding.update({'exp':exp_time})
    token=jwt.encode(encoding,SECRET_KEY,algorithm=ALGORITHM)
    return token

async def get_current_user(token: Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str=payload.get('sub')
        userid:int=payload.get('id')
        userrole:str=payload.get('role')
        if(username is None or userid is None):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate credentials')
        return {'username':username,'id':userid,'role':userrole}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate credentials')

@router.post("/token",response_model=Token)
async def login_for_access_token(db:db_dep, 
            form_data: Annotated[OAuth2PasswordRequestForm,Depends()]):
    user=authenticate_user(db,form_data.username,form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate credentials')
    token=create_access_token(user.username,user.id,user.role,timedelta(minutes=20))
    return {"access_token":token,"token_type":"bearer"}