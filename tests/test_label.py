import pytest

def test_add_label_should_return_success(user_client,token):
    label_data={
        "name": "Personality"
    }
    add_response=user_client.post('/api/labels', json=label_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert add_response.status_code == 201

def test_get_labels_should_return_success(user_client,token):
    label_data={
        "name": "Personality"
    }
    add_response=user_client.post('/api/labels', json=label_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert add_response.status_code == 201
    label_data={
        "name": "Exercise"
    }
    add_response=user_client.post('/api/labels', json=label_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert add_response.status_code == 201
    get_response=user_client.get('/api/labels', headers={"Content-Type": "application/json",
    "Authorization": token})
    assert get_response.status_code == 200

def test_delete_labels_should_return_success(user_client,token):
    label_data={
        "name": "Personality"
    }
    add_response=user_client.post('/api/labels', json=label_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert add_response.status_code == 201
    label_data={
        "name": "Exercise"
    }
    add_response=user_client.post('/api/labels', json=label_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert add_response.status_code == 201
    delete_response=user_client.delete('/api/labels/1', headers={"Content-Type": "application/json",
    "Authorization": token})
    assert delete_response.status_code == 204
    delete_response=user_client.delete('/api/labels/2', headers={"Content-Type": "application/json",
    "Authorization": token})
    assert delete_response.status_code == 204

def test_get_label_should_return_failure(user_client,token):
    get_response=user_client.get('/api/labels', headers={"Content-Type": "application/json",
    "Authorization": token})
    assert get_response.status_code == 404

def test_update_label_should_return_success(user_client,token):
    label_data={
        "name": "Personality"
    }
    add_response=user_client.post('/api/labels', json=label_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert add_response.status_code == 201
    update_data={
        "id":1,
        "name": "Exercise"
    }
    update_response=user_client.put('/api/labels', json=update_data, headers={"Content-Type": "application/json",
    "Authorization": token})
    assert update_response.status_code == 200
    

