from starlette.testclient import TestClient
from app.routers.auth import get_current_user, get_db, return_hash
from .utils import override_get_db,override_user_dependency,test_user,now_time
from app.main import app
from app.routers.users import UserCreate,UserUpdate


client = TestClient(app)
app.dependency_overrides[get_current_user] = override_user_dependency
app.dependency_overrides[get_db] = override_get_db

def test_get_current_user():
    response= client.get('/users/get-user-details')
    assert response.status_code == 200
    assert response.json() == {'user_name': 'Femoo', 'user_id': 1, 'role': 'admin'}

def test_get_all_users(test_user):
    response = client.get('/users/')
    assert response.status_code == 200
    assert response.json()[0].get('id') == 1
    assert response.json()[0].get('user_name') == 'Femi'
    assert response.json()[0].get('email') == 'adefemiadewusi07@gmail.com'
    assert response.json()[0].get('first_name') == 'Adefemi'
    assert response.json()[0].get('last_name') == 'Adewusi'
    assert response.json()[0].get('role') == 'admin'

def test_get_user_by_id(test_user):
    response = client.get('/users/get_user_by_id/1')
    assert response.json().get('id') == 1
    assert response.json().get('user_name') == 'Femi'
    assert response.json().get('email') == 'adefemiadewusi07@gmail.com'
    assert response.json().get('first_name') == 'Adefemi'
    assert response.json().get('last_name') == 'Adewusi'
    assert response.json().get('role') == 'admin'

def test_delete_user(test_user):
    # json_data = {'user_id'}
    response = client.delete('/users/?user_id=1')
    assert response.status_code == 204

# def test_create_new_user():
#     json_data = {
#         'user_name':'Olumide',
#         'email':'olumide@gmail.com',
#         'first_name':'Olumide',
#         'last_name':'Emmanuel',
#         'hashed_password': return_hash('olumzy'),
#         'role':'not admin'
#     }
#     test_model = UserCreate.model_validate(json_data)
#     response = client.post('/users/',json=json_data)
#     assert response.status_code == 201

