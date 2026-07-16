from fastapi import Depends, HTTPException, status, APIRouter, Request
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from starlette.responses import RedirectResponse

from app.database import SessionLocal, get_db
from typing import Annotated
from sqlalchemy.orm import Session
from app.models import User
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi.responses import JSONResponse

router = APIRouter(
    tags=['auth'],
    prefix='/auth'
)


SECRET_KEY = "VRYhv3734yc7vb7387gvu34bv83h"
ALGORITHM= 'HS256'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')
pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Unable to validate user')
db_dependency = Annotated[Session,Depends(get_db)]


def redirect_to_login():
    redirect_response = RedirectResponse('/auth/login')
    redirect_response.delete_cookie('access_token')
    return redirect_response

def authenticate_user(username:str,password:str,db:db_dependency):
    print('Now inside authenticate user')
    user = db.query(User).filter(User.user_name == username).first()
    print('Got the username')
    print(user.user_name)
    print(user.role)
    if user is None:
        raise credential_exception

    if not pwd_context.verify(password, user.hashed_password):
        raise credential_exception

    return user

def create_access_token(username:str,user_id:int,role: str,expires_delta:timedelta):
    try:
        encode = {'sub':username,'id':user_id,'role':role}

        expires = expires_delta + datetime.now(timezone.utc)
        encode.update({'exp':expires})
        token = jwt.encode(encode,SECRET_KEY,ALGORITHM)
        return token

    except JWTError:
        raise credential_exception

@router.post('/token')
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependency):
    # print('I am here')
    user = authenticate_user(form_data.username,form_data.password, db)
    if user is None:
        raise credential_exception

    # print(user.role)

    token = create_access_token(user.user_name,user.id,user.role,timedelta(minutes=20))

    response = JSONResponse({
        'message':'Login successful'
    })
    response.set_cookie(
        key='access_token',
        value=token,
        httponly=False,
        secure=False,
        samesite="Lax"
    )

    return response
    # return {'access_token':token,"token_type":'bearer'}

def return_hash(password):
    password_hash = pwd_context.hash(password)
    return password_hash

def get_current_user(request:Request,token:Annotated[str,Depends(oauth2_scheme)]):
    token = request.cookies.get('access_token')
    print(token)
    payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    user_name: str = payload.get('sub')
    user_id: int = payload.get('id')
    role:str = payload.get('role')

    if user_name is None or user_id is None:
        raise credential_exception
    print({'user_name':user_name,'user_id':user_id,'role':role})
    return {'user_name':user_name,'user_id':user_id,'role':role}

















