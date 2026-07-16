
from typing import Annotated

from fastapi import Depends,HTTPException
from sqlalchemy.orm import Session
from fastapi import APIRouter,status
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.database import SessionLocal, get_db
from pydantic import BaseModel
from app.models import User
from app.routers.auth import get_current_user, credential_exception, pwd_context, return_hash
from passlib.context import CryptContext
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='templates')



router = APIRouter(
    prefix= "/users",
    tags=["users"]
)

class UserCreate(BaseModel):
    user_name:str
    email: str
    first_name:str
    last_name:str
    password: str
    role:str

class UserUpdate(BaseModel):
    user_name:str
    email: str
    first_name:str
    last_name:str
    role:str


user_dependency = Annotated[dict,Depends(get_current_user)]

db_dependency = Annotated[Session,Depends(get_db)]

#PAGES
@router.get('/register-page',)
def render_register_page(request:Request):
    return templates.TemplateResponse(name='register-page.html',request=request)

@router.get('/login-page')
def render_login_page(request:Request):
    return templates.TemplateResponse(name='login-page.html',request=request)


#ENDPOINTS
@router.get("/",status_code=status.HTTP_200_OK)
async def get_all_users(db:db_dependency,user:user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='User not authenticated')
    if user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='User not authorised')

    model = db.query(User).all()
    return model

@router.get("/get_user_by_id/{user_id}",status_code=status.HTTP_200_OK)
async def get_user_by_id(db:db_dependency,user_id,user:user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='User not authenticated')
    if user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='User not authorised')
    model = db.query(User).filter(User.id==user_id).first()
    return model

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(db:db_dependency,user_id):
    model = db.query(User).filter(User.id==user_id).first()
    db.delete(model)

@router.get('/get-user-details')
async def get_user_details(user:user_dependency):
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not authenticated')
        return user

@router.post('/')
async def create_new_user(user:UserCreate,db:db_dependency):
    if user.role != 'admin':
        user.role = 'user'
    new_user = User(user_name=user.user_name,email=user.email,first_name=user.first_name,last_name=user.last_name,hashed_password=return_hash(user.password),role=user.role)
    db.add(new_user)
    db.commit()

@router.put('/')
async def edit_user_details(user:user_dependency, new_details : UserUpdate,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not authenticated')
    model = db.query(User).filter(User.id == user.get('user_id')).first()
    model.user_name = new_details.user_name
    model.email = new_details.email
    model.first_name = new_details.first_name
    model.last_name = new_details.last_name
    db.commit()












