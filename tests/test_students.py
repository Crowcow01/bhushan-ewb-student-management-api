
def sample_student():
    return {
        "name": "Rahul Sharma",
        "email": "rahul.sharma@example.com",
        "age": 21,
        "course": "Civil Engineering",
    }


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_student(client):
    response = client.post("/students/", json=sample_student())
    assert response.status_code == 201
    assert response.json()["name"] == "Rahul Sharma"
    assert response.json()["id"] == 1


def test_list_students(client):
    client.post("/students/", json=sample_student())
    response = client.get("/students/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["email"] == "rahul.sharma@example.com"


def test_retrieve_missing_student(client):
    response = client.get("/students/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found."


def test_update_student(client):
    created = client.post("/students/", json=sample_student())
    student_id = created.json()["id"]

    updated_data = sample_student()
    updated_data["age"] = 22

    response = client.put(
        f"/students/{student_id}",
        json=updated_data,
    )

    assert response.status_code == 200
    assert response.json()["age"] == 22


def test_delete_student(client):
    created = client.post("/students/", json=sample_student())
    student_id = created.json()["id"]

    response = client.delete(f"/students/{student_id}")
    assert response.status_code == 204
    assert client.get(f"/students/{student_id}").status_code == 404


def test_duplicate_email(client):
    client.post("/students/", json=sample_student())

    duplicate = sample_student()
    duplicate["name"] = "Another Student"

    response = client.post("/students/", json=duplicate)
    assert response.status_code == 409
    assert "email already exists" in response.json()["detail"]


def test_invalid_student_input(client):
    invalid_data = {
        "name": "",
        "email": "not-an-email",
        "age": 150,
        "course": "Civil Engineering",
    }

    response = client.post("/students/", json=invalid_data)
    assert response.status_code == 422
