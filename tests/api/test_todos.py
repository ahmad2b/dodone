from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from tests.utils import create_random_todo


def test_create_todo(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    data = {"title": "Foo", "description": "Fighters"}
    response = client.post(
        f"{settings.API_V1_STR}/todos/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "owner" in content and "id" in content["owner"]


def test_read_todo(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    todo = create_random_todo(db)
    response = client.get(
        f"{settings.API_V1_STR}/todos/{todo.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == todo.title
    assert content["description"] == todo.description
    assert content["id"] == todo.id
    assert "owner" in content and "id" in content["owner"]


def test_read_todo_not_found(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/todos/999",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Todo not found"


def test_read_todo_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    todo = create_random_todo(db)
    response = client.get(
        f"{settings.API_V1_STR}/todos/{todo.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_read_todos(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    create_random_todo(db)
    create_random_todo(db)
    response = client.get(
        f"{settings.API_V1_STR}/todos/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) >= 2


def test_update_todo(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    todo = create_random_todo(db)
    data = {"title": "Updated title", "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/todos/{todo.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert content["id"] == todo.id
    assert "owner" in content and "id" in content["owner"]


def test_update_todo_not_found(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    data = {"title": "Updated title", "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/todos/999",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Todo not found"


def test_update_todo_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    todo = create_random_todo(db)
    data = {"title": "Updated title", "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/todos/{todo.id}",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_delete_todo(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    todo = create_random_todo(db)
    response = client.delete(
        f"{settings.API_V1_STR}/todos/{todo.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Todo deleted successfully"


def test_delete_todo_not_found(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/todos/999",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Todo not found"


def test_delete_item_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    todo = create_random_todo(db)
    response = client.delete(
        f"{settings.API_V1_STR}/todos/{todo.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"