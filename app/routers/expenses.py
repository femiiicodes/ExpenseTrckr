from typing import Annotated
from xmlrpc.client import DateTime
from collections import defaultdict
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from starlette import status
from starlette.responses import RedirectResponse

from app.database import SessionLocal, get_db
from app.models import Expense
from app.routers.auth import get_current_user
from datetime import datetime
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory='templates')

router = APIRouter(
    prefix="/expenses",
    tags=["expenses"]
)

user_dependency = Annotated[dict, Depends(get_current_user)]

Session=SessionLocal()

class ExpenseCreate(BaseModel):
    amount: float
    title: str

def redirect_to_login():
    redirect_response = RedirectResponse('/auth/login')
    redirect_response.delete_cookie('access_token')
    return redirect_response

db_dependency = Annotated[Session,Depends(get_db)]
### PAGES ###
@router.get('/expenses-page')
async def render_expenses_page(request:Request,db:db_dependency,):
    token = request.cookies.get('access_token')
    print(token)
    user = get_current_user(token=token,request=request)
    print(user.get('role'))
    username = user.get('user_name')
    expenses = db.query(Expense).filter(Expense.owner_id == user.get('user_id')).order_by(Expense.time).all()
    expenses_by_day = defaultdict(list)
    for expense in expenses:
        day = expense.time.date()
        expenses_by_day[day].append(expense)


    grouped_items = []
    for date,expenses in expenses_by_day.items():
        grouped_items.append({
            'day':date,
            'total': sum(exp.amount for exp in expenses),
            'expenses':expenses
        })


    today = datetime.now().date()
    today_exists = any(item["day"] == today for item in grouped_items)
    print(expenses_by_day)
    return templates.TemplateResponse(
        name="expenses-page.html",
        request=request,
        context={
            "today": today,
            "today_exists": today_exists,
            "username": username,
            "expenses_by_day": expenses_by_day,
            "grouped_items": grouped_items
        }
    )

@router.get('/edit-expense-page/{expense_id}')
def render_edit_expense_page(request:Request,expense_id:int):
    return templates.TemplateResponse(name='edit-expense.html',request=request,context={})

@router.get('/add-expense-page')
def render_create_expense_page(request:Request):
    return templates.TemplateResponse(name='create-expense.html',request=request)


### ROUTES ###
@router.get("/",status_code=status.HTTP_200_OK)
async def get_all_expenses(db:db_dependency,user:user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='User not authenticated')
    if user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='User not authorized')
    model = db.query(Expense).all()
    return model

@router.get("/my-expenses",status_code=status.HTTP_200_OK)
async def get_my_expenses(db:db_dependency,user:user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='User not authenticated')
    model = db.query(Expense).filter(user.get('user_id') == Expense.owner_id).all()
    return model

@router.get("/get_expense_by_id/{expense_id}",status_code=status.HTTP_200_OK)
async def get_expense_by_id(expense_id,db:db_dependency,user:user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='User not authenticated')
    model = db.query(Expense).filter(Expense.id==expense_id).first()
    if user.get('user_id') != model.owner_id and user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='User not authorized')
    if model is not None:
        return model
    raise HTTPException(status_code=404,detail="Expense with that id not found")

@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_expense(expense:ExpenseCreate,db:db_dependency,user:user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='User not authenticated')
    expense=Expense(amount=expense.amount,title=expense.title,time=datetime.now(),owner_id=user.get('user_id'))
    db.add(expense)
    db.commit()

@router.put("/update/{expense_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_expense(expense_id,new_expense:ExpenseCreate,db:db_dependency,user:user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='User not authenticated')
    if db.query(Expense).filter(Expense.id==expense_id).first() is not None:
        model = db.query(Expense).filter(Expense.id == expense_id).first()
        if user.get('user_id') != model.owner_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not authorized')
        model.amount = new_expense.amount
        model.title = new_expense.title
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Expense with that id not found")

@router.delete("/delete/{expense_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(expense_id,db:db_dependency,user:user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='User not authenticated')


    model = db.query(Expense).filter(Expense.id == expense_id).first()

    if model is not None:
        if model.owner_id != user.get('user_id') and user.get('role') != 'admin':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not authorized')
        db.delete(model)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Expense with that id not found ")





