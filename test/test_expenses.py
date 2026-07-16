from test.test_users import client
from test.utils import test_expense
from datetime import datetime

def test_get_my_expenses(test_expense):
    response = client.get('/expenses/')
    assert response.status_code == 200
    response_json = response.json()[0]
    assert response_json.get('id') == 1
    assert response_json.get('amount') == 3000
    assert response_json.get('title') == 'Ewa G'

def test_get_expense_by_id(test_expense):
    response = client.get('/expenses/get_expense_by_id/1')
    assert response.status_code == 200
    assert response.json().get('id') == 1
    assert response.json().get('amount') == 3000
    assert response.json().get('title') == 'Ewa G'





