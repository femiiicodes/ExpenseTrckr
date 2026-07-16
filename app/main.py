from typing import Annotated
from xmlrpc.client import DateTime

from fastapi import FastAPI,status, Request
from fastapi.params import Depends
from fastapi.templating import Jinja2Templates

from app.database import SessionLocal
from pydantic import BaseModel, Field
from app.models import Expense
from app.routers import expenses,users, auth
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()
app.mount('/static',StaticFiles(directory='static'),name='static')
template = Jinja2Templates(directory = 'templates')

@app.get('/home-page')
def render_index_page(request:Request):
    return template.TemplateResponse(name='index.html',request=request)

@app.get('/')
def home_page(request:Request):
    return RedirectResponse('/home-page',status.HTTP_302_FOUND)


app.include_router(expenses.router)
app.include_router(users.router)
app.include_router(auth.router)




