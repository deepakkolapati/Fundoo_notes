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
    assert login_response.status_code == 200  
    note_data={
        "title": "top movies",
        "description": "inception",
        "color":"yellow"
    }
    note_response = user_client.post('/api/notes', json=note_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert note_response.status_code == 201 

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
    assert login_response.status_code == 200  
    note_data={
        "title": "top movies",
        "description": "inception",
        "color":"yellow"
    }
    note_response = user_client.post('/api/notes', json=note_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert note_response.status_code == 201 
    notes_get_response = user_client.get('/api/notes', headers={"Content-Type": "application/json","Authorization": token})
    assert notes_get_response.status_code == 200
    print(notes_get_response.json)
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
    assert login_response.status_code == 200  
    note_data={
        "title": "top movies",
        "description": "inception",
        "color":"yellow"
    }
    note_response = user_client.post('/api/notes', json=note_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert note_response.status_code == 201 
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
    assert login_response.status_code == 200  
    note_data={
        "title": "top movies",
        "description": "inception",
        "color":"yellow"
    }
    note_response = user_client.post('/api/notes', json=note_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert note_response.status_code == 201 
    note_data={
        "title": "top series",
        "description": "The office",
        "color":"red"
    }
    note_response = user_client.post('/api/notes', json=note_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert note_response.status_code == 201 
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
    assert login_response.status_code == 200  
    note_data={
        "title": "top movies",
        "description": "inception",
        "color":"yellow"
    }
    note_response = user_client.post('/api/notes', json=note_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert note_response.status_code == 201 
    note_data={
        "title": "top series",
        "description": "The office",
        "color":"yellow"
    }
    note_response = user_client.post('/api/notes', json=note_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert note_response.status_code == 201 
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
    assert login_response.status_code == 200  
    note_data={
        "title": "top movies",
        "description": "inception",
        "color":"yellow"
    }
    note_response = user_client.post('/api/notes', json=note_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert note_response.status_code == 201 
    archive_data={"id" : 1}
    archive_response=user_client.patch('/api/archive',json=archive_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert archive_response.status_code == 200
    assert archive_response.json['message'] == 'Note is archived'

def test_unarchive_note_should_return_success(user_client):
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
    assert login_response.status_code == 200  
    note_data={
        "title": "top movies",
        "description": "inception",
        "color":"yellow"
    }
    note_response = user_client.post('/api/notes', json=note_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert note_response.status_code == 201 
    archive_data={"id" : 1}
    archive_response=user_client.patch('/api/archive',json=archive_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert archive_response.status_code == 200
    assert archive_response.json['message'] == 'Note is archived'
    un_archive_response=user_client.patch('/api/archive',json=archive_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert un_archive_response.status_code == 200
    assert un_archive_response.json['message'] == 'Note is unarchived'

   

def test_get_archived_notes_should_return_success(user_client):
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
    assert login_response.status_code == 200  
    note_data={
        "title": "top movies",
        "description": "inception",
        "color":"yellow"
    }
    note_response = user_client.post('/api/notes', json=note_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert note_response.status_code == 201 
    note_data={
        "title": "top series",
        "description": "The office",
        "color":"yellow"
    }
    note_response = user_client.post('/api/notes', json=note_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert note_response.status_code == 201 
    archive_data={"id" : 1}
    archive_response=user_client.patch('/api/archive',json=archive_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert archive_response.status_code == 200
    assert archive_response.json['message'] == 'Note is archived'
    archive_data={"id" : 2}
    archive_response=user_client.patch('/api/archive',json=archive_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert archive_response.status_code == 200
    assert archive_response.json['message'] == 'Note is archived'
    get_archive_notes_response=user_client.get('/api/archive', headers={"Content-Type": "application/json",
    "Authorization": token})
    assert get_archive_notes_response.status_code == 200
    assert get_archive_notes_response.json['message'] == 'Retrieved archive notes'
    assert isinstance(get_archive_notes_response.json['data'], list)

def test_archive_note_not_found_should_return_success(user_client):
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
    assert login_response.status_code == 200  
    note_data={
        "title": "top movies",
        "description": "inception",
        "color":"yellow"
    }
    note_response = user_client.post('/api/notes', json=note_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert note_response.status_code == 201
    note_data={
        "title": "top series",
        "description": "The office",
        "color":"yellow"
    }
    note_response = user_client.post('/api/notes', json=note_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert note_response.status_code == 201
    get_archive_notes_response=user_client.get('/api/archive', headers={"Content-Type": "application/json",
    "Authorization": token})
    assert get_archive_notes_response.status_code == 404
    assert get_archive_notes_response.json['message'] == 'Notes not found'



def test_trash_note_should_return_success(user_client):
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
    assert login_response.status_code == 200  
    note_data={
        "title": "top movies",
        "description": "inception",
        "color":"yellow"
    }
    note_response = user_client.post('/api/notes', json=note_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert note_response.status_code == 201 
    trash_data={"id" : 1}
    trash_response=user_client.patch('/api/trash',json=trash_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert trash_response.status_code == 200
    assert trash_response.json['message'] == 'Note moved to Trash'

def test_restore_trash_note_should_return_success(user_client):
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
    assert login_response.status_code == 200  
    note_data={
        "title": "top movies",
        "description": "inception",
        "color":"yellow"
    }
    note_response = user_client.post('/api/notes', json=note_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert note_response.status_code == 201 
    trash_data={"id" : 1}
    trash_response=user_client.patch('/api/trash',json=trash_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert trash_response.status_code == 200
    assert trash_response.json['message'] == 'Note moved to Trash'
    restore_trash_response=user_client.patch('/api/trash',json=trash_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert restore_trash_response.status_code == 200
    assert restore_trash_response.json['message'] == 'Note is restored'



def test_get_trash_notes_should_return_success(user_client):
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
    assert login_response.status_code == 200  
    note_data={
        "title": "top movies",
        "description": "inception",
        "color":"yellow"
    }
    note_response = user_client.post('/api/notes', json=note_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert note_response.status_code == 201 
    note_data={
        "title": "top series",
        "description": "The office",
        "color":"yellow"
    }
    note_response = user_client.post('/api/notes', json=note_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert note_response.status_code == 201 
    trash_data={"id" : 1}
    trash_response=user_client.patch('/api/trash',json=trash_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert trash_response.status_code == 200
    assert trash_response.json['message'] == 'Note moved to Trash'
    trash_data={"id" : 2}
    trash_response=user_client.patch('/api/trash',json=trash_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert trash_response.status_code == 200
    assert trash_response.json['message'] == 'Note moved to Trash'
    get_trash_notes_response=user_client.get('/api/trash', headers={"Content-Type": "application/json",
    "Authorization": token})
    assert get_trash_notes_response.status_code == 200
    assert get_trash_notes_response.json['message'] == 'Retrieved trash notes'
    assert isinstance(get_trash_notes_response.json['data'], list)

def test_trash_note_not_found_should_return_success(user_client):
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
    assert login_response.status_code == 200  
    note_data={
        "title": "top movies",
        "description": "inception",
        "color":"yellow"
    }
    note_response = user_client.post('/api/notes', json=note_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert note_response.status_code == 201
    note_data={
        "title": "top series",
        "description": "The office",
        "color":"yellow"
    }
    note_response = user_client.post('/api/notes', json=note_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert note_response.status_code == 201
    get_trash_notes_response=user_client.get('/api/trash', headers={"Content-Type": "application/json",
    "Authorization": token})
    assert get_trash_notes_response.status_code == 404
    assert get_trash_notes_response.json['message'] == 'Notes not found'