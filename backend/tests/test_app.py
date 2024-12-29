import pytest
from backend.app import app  

@pytest.fixture

 # Flask test client for simulating API requests
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Tests the home route to ensure the API is running
def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"FinanceTracker API is running!" in response.data

# Tests creating a group with valid data
def test_create_group_valid(client):
    response = client.post('/groups', json={'GroupName': 'Test Group'})
    assert response.status_code == 201
    assert response.json['message'] == 'Group created successfully!'

# Tests creating a group without a name (invalid request)
def test_create_group_invalid(client):
    response = client.post('/groups', json={})
    assert response.status_code == 400
    assert 'Group name is required!' in response.json['error']

# Tests fetching the list of groups
def test_get_groups(client):
    response = client.get('/groups')
    assert response.status_code == 200
    assert isinstance(response.json, list)

# Tests creating a user with valid data
def test_create_user_valid(client):
    response = client.post('/users', json={
        'name': 'John Doe',
        'email': 'unique.johnnew@example.com',  # Unique email is required !
        'password': 'securepassword',
        'currency': 'USD'
    })
    assert response.status_code == 201
    assert 'User added successfully!' in response.json['message']

# Tests creating a user with missing fields
def test_create_user_invalid(client):
    response = client.post('/users', json={
        'email': 'john.doe@example.com',
    })
    assert response.status_code == 400
    assert 'Name, email, and password are required!' in response.json['error']

# Tests fetching the list of users
def test_get_users(client):
    response = client.get('/users')
    assert response.status_code == 200
    assert isinstance(response.json, list)

# Tests creating a group with a name exceeding character limits
def test_create_group_long_name(client):
    long_name = "A" * 256  # 256 characters long
    response = client.post('/groups', json={'GroupName': long_name})
    assert response.status_code == 400
    assert 'Group name must not exceed 255 characters!' in response.json['error']

# Tests creating duplicate groups to ensure uniqueness constraint
def test_create_duplicate_group(client):
    group_name = "Duplicate Group"
    client.post('/groups', json={'GroupName': group_name})  # First creation
    response = client.post('/groups', json={'GroupName': group_name})  # Duplicate creation
    assert response.status_code == 400
    assert 'Group with this name already exists!' in response.json['error']

# Tests creating users with duplicate emails
def test_create_duplicate_user(client):
    email = "duplicate@example.com"
    client.post('/users', json={
        'name': 'Jane Doe',
        'email': email,                     
        'password': 'password123',
        'currency': 'USD'
    })  # İlk kullanıcı
    response = client.post('/users', json={
        'name': 'Another User',
        'email': email,  # Aynı email
        'password': 'anotherpassword',
        'currency': 'EUR'
    })
    assert response.status_code == 500
    assert 'unique constraint' in response.json['error'].lower()

# Tests updating a non-existent user
def test_update_nonexistent_user(client):
    response = client.put('/users/9999/password', json={'password': 'newpassword'})
    assert response.status_code == 404                      ####
    assert 'User not found!' in response.json['error']

# Tests creating an expense with a negative amount
def test_create_expense_negative_amount(client):
    response = client.post('/expenses', json={
        'group_id': 1,
        'user_id': 1,                          
        'amount': -50.00,  # Negatif amount
        'description': 'Invalid Expense'
    })
    assert response.status_code == 400
    assert 'Amount must be greater than zero!' in response.json['error']

# Tests creating an expense for a non-existent group
def test_create_expense_invalid_group(client):
    response = client.post('/expenses', json={
        'group_id': 9999,  # Nonexistent group ID
        'user_id': 1,
        'amount': 50.00,                            
        'description': 'Expense for invalid group'
    })
    assert response.status_code == 400
    assert 'Group ID does not exist!' in response.json['error']

# Tests creating a notification for a user
def test_create_notification(client):
    response = client.post('/notifications', json={
        'user_id': 38 ,  # Ensure user_id 1 exists in your Users table
        'message': 'Test Notification'
    })
    assert response.status_code == 201
    assert 'Notification created successfully!' in response.json['message']

# Tests fetching a notification that doesn't exist
def test_get_nonexistent_notification(client):
    response = client.get('/notifications/9999')
    assert response.status_code == 404                          
    assert 'Notification not found!' in response.json['error']

# Tests marking a notification as read
def test_mark_notification_as_read(client):
    # Create a notification
    response = client.post('/notifications', json={
        'user_id': 38,  # Ensure this user exists in the Users table
        'message': 'Test Notification to Mark as Read'
    })

    print("Response JSON:", response.json)  # Debug the response
    assert response.status_code == 201

    # Extract notification_id from the response
    notification_id = response.json['notification_id']
    assert notification_id is not None, "Notification ID should not be None"

    # Mark the notification as read
    response = client.put(f'/notifications/{notification_id}')
    assert response.status_code == 200
    assert response.json['message'] == 'Notification marked as