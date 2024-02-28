import pytest

def test_add_note_should_return_success(user_client):
    register_data = {
        "username": "Karan",
        "email": "joshikfelix22@gmail.com",
        "password": "Kc5656$ef",
        "location": "srm"
    }
    user_client.post('/api/user', json=register_data, headers={"Content-Type": "application/json"})
    login_data = {
        "username": "Karan",
        "password": "Kc5656$ef"
    }
    login_response = user_client.post('/api/login', json=login_data, headers={"Content-Type": "application/json"})
    token=login_response.json['token']
    assert login_response.status_code == 200  # OK
    note_data={
        "title": "top movies",
        "description": "inception",
        "color":"yellow"
    }
    note_response = user_client.post('/api/notes', json=note_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert note_response.status_code == 201 # OK

def test_get_notes_should_return_success(user_client):
    register_data = {
        "username": "Karan",
        "email": "joshikfelix22@gmail.com",
        "password": "Kc5656$ef",
        "location": "srm"
    }
    user_client.post('/api/user', json=register_data, headers={"Content-Type": "application/json"})
    login_data = {
        "username": "Karan",
        "password": "Kc5656$ef"
    }
    login_response = user_client.post('/api/login', json=login_data, headers={"Content-Type": "application/json"})
    token=login_response.json['token']
    assert login_response.status_code == 200  # OK
    note_data={
        "title": "top movies",
        "description": "inception",
        "color":"yellow"
    }
    note_response = user_client.post('/api/notes', json=note_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert note_response.status_code == 201 # OK
    notes_get_response = user_client.get('/api/notes', headers={"Content-Type": "application/json","Authorization": token})
    assert notes_get_response.status_code == 200
    assert notes_get_response.json['message'] == 'Notes Found'

def test_update_note_should_return_suceess(user_client):
    register_data = {
        "username": "Karan",
        "email": "joshikfelix22@gmail.com",
        "password": "Kc5656$ef",
        "location": "srm"
    }
    user_client.post('/api/user', json=register_data, headers={"Content-Type": "application/json"})
    login_data = {
        "username": "Karan",
        "password": "Kc5656$ef"
    }
    login_response = user_client.post('/api/login', json=login_data, headers={"Content-Type": "application/json"})
    token=login_response.json['token']
    assert login_response.status_code == 200  # OK
    note_data={
        "title": "top movies",
        "description": "inception",
        "color":"yellow"
    }
    note_response = user_client.post('/api/notes', json=note_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert note_response.status_code == 201 # OK
    note_update_data = {
        "id":1,
        "title": "updated title",
        "description": "updated description",
        "color": "blue"
    }
    update_response = user_client.put('/api/notes',json=note_update_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert update_response.status_code == 200
    assert update_response.json['message'] == 'Note updated successfully'

def test_get_single_note_should_return_success(user_client):
    register_data = {
        "username": "Karan",
        "email": "joshikfelix22@gmail.com",
        "password": "Kc5656$ef",
        "location": "srm"
    }
    user_client.post('/api/user', json=register_data, headers={"Content-Type": "application/json"})
    login_data = {
        "username": "Karan",
        "password": "Kc5656$ef"
    }
    login_response = user_client.post('/api/login', json=login_data, headers={"Content-Type": "application/json"})
    token=login_response.json['token']
    assert login_response.status_code == 200  # OK
    note_data={
        "title": "top movies",
        "description": "inception",
        "color":"yellow"
    }
    note_response = user_client.post('/api/notes', json=note_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert note_response.status_code == 201 # OK
    note_data={
        "title": "top series",
        "description": "The office",
        "color":"red"
    }
    note_response = user_client.post('/api/notes', json=note_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert note_response.status_code == 201 # OK
    get_single_response = user_client.get('/api/notes/1', headers={"Content-Type": "application/json","Authorization": token})
    assert get_single_response.status_code == 200
    assert get_single_response.json['message'] == 'Notes found' or get_single_response.json['message'] == 'Shared Notes found'

def test_delete_note_should_return_success(user_client):
    register_data = {
        "username": "Karan",
        "email": "joshikfelix22@gmail.com",
        "password": "Kc5656$ef",
        "location": "srm"
    }
    user_client.post('/api/user', json=register_data, headers={"Content-Type": "application/json"})
    login_data = {
        "username": "Karan",
        "password": "Kc5656$ef"
    }
    login_response = user_client.post('/api/login', json=login_data, headers={"Content-Type": "application/json"})
    token=login_response.json['token']
    assert login_response.status_code == 200  # OK
    note_data={
        "title": "top movies",
        "description": "inception",
        "color":"yellow"
    }
    note_response = user_client.post('/api/notes', json=note_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert note_response.status_code == 201 # OK
    note_data={
        "title": "top series",
        "description": "The office",
        "color":"yellow"
    }
    note_response = user_client.post('/api/notes', json=note_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert note_response.status_code == 201 # OK
    delete_response = user_client.delete('/api/notes/2', headers={"Content-Type": "application/json","Authorization": token})
    assert delete_response.status_code == 204
    
def test_archive_note_should_return_success(user_client):
    register_data = {
        "username": "Karan",
        "email": "joshikfelix22@gmail.com",
        "password": "Kc5656$ef",
        "location": "srm"
    }
    user_client.post('/api/user', json=register_data, headers={"Content-Type": "application/json"})
    login_data = {
        "username": "Karan",
        "password": "Kc5656$ef"
    }
    login_response = user_client.post('/api/login', json=login_data, headers={"Content-Type": "application/json"})
    token=login_response.json['token']
    assert login_response.status_code == 200  # OK
    note_data={
        "title": "top movies",
        "description": "inception",
        "color":"yellow"
    }
    note_response = user_client.post('/api/notes', json=note_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert note_response.status_code == 201 # OK
    archive_data={"id" : 1}
    archive_response=user_client.patch('/api/archive',json=archive_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert archive_response.status_code == 200
    assert archive_response.json['message'] == 'Note is archived'
