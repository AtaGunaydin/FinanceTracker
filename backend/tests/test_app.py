import pytest
from backend.app import app  

@pytest.fixture

def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"FinanceTracker API is running!" in response.data

def test_create_group_valid(client):
    response = client.post('/groups', json={'GroupName': 'Test Group'})
    assert response.status_code == 201
    assert response.json['message'] == 'Group created successfully!'

def test_create_group_invalid(client):
    response = client.post('/groups', json={})
    assert response.status_code == 400
    assert 'Group name is required!' in response.json['error']

def test_get_groups(client):
    response = client.get('/groups')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_user_valid(client):
    response = client.post('/users', json={
        'name': 'John Doe',
        'email': 'unique.johnnew@example.com', 
        'password': 'securepassword',
        'currency': 'USD'
    })
    assert response.status_code == 201
    assert 'User added successfully!' in response.json['message']

def test_create_user_invalid(client):
    response = client.post('/users', json={
        'email': 'john.doe@example.com',
    })
    assert response.status_code == 400
    assert 'Name, email, and password are required!' in response.json['error']

def test_get_users(client):
    response = client.get('/users')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_group_long_name(client):
    long_name = "A" * 256  
    response = client.post('/groups', json={'GroupName': long_name})
    assert response.status_code == 400
    assert 'Group name must not exceed 255 characters!' in response.json['error']

def test_create_duplicate_group(client):
    group_name = "Duplicate Group"
    client.post('/groups', json={'GroupName': group_name})  
    response = client.post('/groups', json={'GroupName': group_name}) 
    assert response.status_code == 400
    assert 'Group with this name already exists!' in response.json['error']

def test_create_duplicate_user(client):
    email = "duplicate@example.com"
    client.post('/users', json={
        'name': 'Jane Doe',
        'email': email,                     
        'password': 'password123',
        'currency': 'USD'
    }) 
    response = client.post('/users', json={
        'name': 'Another User',
        'email': email,  
        'password': 'anotherpassword',
        'currency': 'EUR'
    })
    assert response.status_code == 500
    assert 'unique constraint' in response.json['error'].lower()

def test_update_nonexistent_user(client):
    response = client.put('/users/9999/password', json={'password': 'newpassword'})
    assert response.status_code == 404                     
    assert 'User not found!' in response.json['error']

def test_create_expense_negative_amount(client):
    response = client.post('/expenses', json={
        'group_id': 1,
        'user_id': 1,                          
        'amount': -50.00,  
        'description': 'Invalid Expense'
    })
    assert response.status_code == 400
    assert 'Amount must be greater than zero!' in response.json['error']

def test_create_expense_invalid_group(client):
    response = client.post('/expenses', json={
        'group_id': 9999, 
        'user_id': 1,
        'amount': 50.00,                            
        'description': 'Expense for invalid group'
    })
    assert response.status_code == 400
    assert 'Group ID does not exist!' in response.json['error']

def test_create_notification(client):
    response = client.post('/notifications', json={
        'user_id': 38 , 
        'message': 'Test Notification'
    })
    assert response.status_code == 201
    assert 'Notification created successfully!' in response.json['message']

def test_get_nonexistent_notification(client):
    response = client.get('/notifications/9999')
    assert response.status_code == 404                          
    assert 'Notification not found!' in response.json['error']

def test_mark_notification_as_read(client):
    response = client.post('/notifications', json={
        'user_id': 38, 
        'message': 'Test Notification to Mark as Read'
    })

    print("Response JSON:", response.json) 
    assert response.status_code == 201

    notification_id = response.json['notification_id']
    assert notification_id is not None, "Notification ID should not be None"

    response = client.put(f'/notifications/{notification_id}')
    assert response.status_code == 200
    assert response.json['message'] == 'Notification marked as read!'

def test_create_debt(client):
    response = client.post('/debts', json={
        'from_user_id': 38,
        'to_user_id': 40,
        'amount': 100.00
    })
    assert response.status_code == 201
    assert 'Debt created successfully!' in response.json['message'] 

def test_create_debt_invalid_amount(client):
    response = client.post('/debts', json={
        'from_user_id': 38,
        'to_user_id': 40,                       
        'amount': -10.00  
    })
    assert response.status_code == 400
    assert 'Amount must be greater than zero!' in response.json['error']

def test_invalid_route(client):
    response = client.get('/invalidroute')          
    assert response.status_code == 404
