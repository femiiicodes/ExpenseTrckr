# from datetime import timedelta
#
# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from starlette.testclient import TestClient
#
# from app.models import Base
# from app.main import app
# from app.database import get_db
# from passlib.context import CryptContext
#
# from app.routers.auth import get_current_user
# from app.routers.users import user_dependency
#
# pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
#
# TEST_DATABASE_URL = 'sqlite:///./testing.db'
#
#
# @pytest.fixture
# def engine():
#     engine = create_engine(TEST_DATABASE_URL,connect_args={'check_same_thread':False})
#     Base.metadata.create_all(bind=engine)
#     yield engine
#     Base.metadata.drop_all(bind=engine)
#
# @pytest.fixture
# def db_session(engine):
#     TestingSessionLocal = sessionmaker(bind=engine,autoflush=False,autocommit=False)
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
# def override_user_dependency():
#     return {'user_name': 'Femoo', 'user_id': 1, 'role': 'admin'}
#
#
# @pytest.fixture
# def client(db_session):
#     def test_get_db():
#         try:
#             yield db_session
#         finally:
#             db_session.close()
#
#         app.dependency_overrides[get_db] = test_get_db
#         app.dependency_overrides[get_current_user] = override_user_dependency
#
#     with TestClient(app) as c:
#         yield c
#         app.dependency_overrides = {}
#
# @pytest.fixture
# def sample_user(db_session):
#     from app.models import User
#
#     user = User(user_name='Femoo',email='adefemi@gmail.com',first_name='Adefemi',last_name='Adewusi',hashed_password=pwd_context.hash('test123'),role='admin')
#     db_session.add(user)
#     db_session.commit()
#     db_session.refresh(user)
#
#     yield user
#
#     db_session.query(User).filter(User.user_name=='Femoo').delete()
#     db_session.commit()
from datetime import datetime
from typing import Annotated

import pytest
from fastapi import Depends
#
# @pytest.fixture
# def token_header(sample_user):
#     """Generate a valid authentication token for the sample user."""
#     from app.routers.auth import create_access_token
#
#     access_token = create_access_token(sample_user.user_name,sample_user.id,sample_user.role,timedelta(minutes=20))
#     return {'access_token':access_token,"token_type":'bearer'}
#
#
#
# @pytest.fixture
# def authenticated_client(client, token_header):
#     """Client that includes authentication headers with each request."""
#     client.headers.update(token_header)
#     return client

from sqlalchemy.orm import sessionmaker, Session

from app import models
from sqlalchemy import create_engine, text

from app.models import User, Expense
from app.routers.auth import return_hash

SQLALCHEMY_URL = 'sqlite:///./testing.db'

engine = create_engine(SQLALCHEMY_URL,connect_args={'check_same_thread':False})
TestingSessionLocal = sessionmaker(bind=engine,autoflush=False,autocommit=False)
models.Base.metadata.create_all(bind=engine)


def override_user_dependency():
    return {'user_name': 'Femoo', 'user_id': 1, 'role': 'admin'}

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

now_time =  datetime(2026, 6, 11, 14, 21, 31, 424340)

@pytest.fixture
def test_user():
    user = User(
        id=1,
        user_name='Femi',
        email='adefemiadewusi07@gmail.com',
        first_name='Adefemi',
        last_name='Adewusi',
        hashed_password=return_hash('test123'),
        role='admin'
    )
    db=TestingSessionLocal()
    db.add(user)
    db.commit()

    yield db
    with engine.connect() as c:
        c.execute(text('DELETE FROM users'))
        c.commit()

@pytest.fixture
def test_expense():
    expense = Expense(
        id=1,
        amount=3000,
        title='Ewa G',
        time=now_time,
        owner_id=1)

    db=TestingSessionLocal()

    db.add(expense)
    db.commit()
    yield db

    with engine.connect() as c:
        c.execute(text('DELETE FROM expenses'))
        c.commit()

