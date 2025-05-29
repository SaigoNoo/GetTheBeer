import pytest
from unittest.mock import MagicMock

from api.user import Users
from api.models import CreateUser


# je Mock la db
class MockDB:
    def __init__(self):
        self.call_function = MagicMock()
        self.call_procedure = MagicMock()


@pytest.fixture
def mock_db():
    return MockDB()


@pytest.fixture
def users(mock_db):
    return Users(db=mock_db)


def test_test_get_all_users(users, mock_db):
    mock_db.call_function.return_value = [
        {"username": "user1"},
        {"username": "user2"}
    ]
    result = users.test_get_all_users()
    assert isinstance(result, list)
    assert result[0]["username"] == "user1"
    mock_db.call_function.assert_called_with(
        name="get_all_users", to_json=True
    )


def test_get_email_from_username_or_email(users, mock_db):
    mock_db.call_function.side_effect = lambda name, **kwargs: (
        1 if name == "user_exists" and kwargs.get("username") == "user1" else
        1 if name == "id_of_user" and kwargs.get("username") == "user1" else
        {"email": "test@example.com"}
        if name == "get_user_info_by_id" and kwargs.get("id") == 1 else
        None
    )
    email = users.get_email_from_username_or_email("user1")
    assert email == "test@example.com"


def test_get_email_invalid_username(users, mock_db):
    mock_db.call_function.return_value = 0
    assert users.get_email_from_username_or_email("") is None


def test_generate_token():
    token = Users.generate_token()
    assert token is not None


def test_ask_reset_user_exists_and_active_token(users, mock_db):
    mock_db.call_function.side_effect = lambda name, **kwargs: (
        1 if name == "user_exists" else
        1 if name == "is_active_token" else
        1 if name == "id_of_user" else
        {"email": "user1@example.com"} if name == "get_user_info_by_id" else
        None
    )
    response = users.ask_reset(email="user1")
    assert "déjà été effectuée" in response


def test_ask_reset_user_does_not_exist(users, mock_db):
    mock_db.call_function.return_value = 0
    response = users.ask_reset(email="nonexistent")
    assert "erreur" in response.lower() or "inconnu" in response.lower()


def test_ask_reset_invalid_email(users, mock_db):
    with pytest.raises(Exception):
        users.ask_reset(email=None)


def test_create_user_success(users, mock_db):
    data = CreateUser(
        username="newuser",
        password="password",
        url_avatar="avatar.png",
        last_name="Doe",
        first_name="John",
        email="john@example.com",
        is_admin=False
    )
    mock_db.call_function.return_value = 0
    response = users.create_user(data)
    mock_db.call_procedure.assert_called_once()
    assert "succès" in response["message"].lower()


def test_create_user_exists(users, mock_db):
    data = CreateUser(
        username="existinguser",
        password="password",
        url_avatar="avatar.png",
        last_name="Doe",
        first_name="John",
        email="john@example.com",
        is_admin=False
    )
    mock_db.call_function.return_value = 1
    with pytest.raises(Exception) as exc_info:
        users.create_user(data)
    assert "existe déjà" in str(exc_info.value)


def test_login_user_success(users, mock_db):
    mock_db.call_function.side_effect = lambda name, **kwargs: (
        1 if name == "user_exists" else
        "password" if name == "get_user_password" else
        None
    )
    result = users.login_user("user", "password")
    assert "réussie" in result["message"].lower()


def test_login_user_wrong_password(users, mock_db):
    mock_db.call_function.side_effect = lambda name, **kwargs: (
        1 if name == "user_exists" else
        "password" if name == "get_user_password" else
        None
    )
    with pytest.raises(Exception):
        users.login_user("user", "wrongpassword")


def test_login_user_not_exist(users, mock_db):
    mock_db.call_function.side_effect = (
        lambda name, **kwargs: 0 if name == "user_exists" else None
    )
    with pytest.raises(Exception):
        users.login_user("nouser", "password")


def test_add_friend_success(users, mock_db):
    mock_db.call_function.side_effect = lambda name, **kwargs: (
        1 if name == "user_exists" else
        0 if name == "is_friend" else
        None
    )
    users.db.call_procedure = MagicMock()
    response = users.add_friend(1, 2)
    assert "succès" in response["message"].lower()
    users.db.call_procedure.assert_called_once_with(
        name="add_friend", user_id=1, friend_id=2
    )


def test_add_friend_already_friends(users, mock_db):
    mock_db.call_function.side_effect = lambda name, **kwargs: (
        1 if name == "user_exists" else
        1 if name == "is_friend" else
        None
    )
    with pytest.raises(Exception):
        users.add_friend(1, 2)


def test_add_friend_same_user(users, mock_db):
    with pytest.raises(Exception):
        users.add_friend(1, 1)


def test_delete_friend_success(users, mock_db):
    mock_db.call_function.side_effect = lambda name, **kwargs: (
        1 if name == "user_exists" else
        1 if name == "is_friend" else
        None
    )
    users.db.call_procedure = MagicMock()
    response = users.delete_friend(1, 2)
    assert "succès" in response["message"].lower()
    users.db.call_procedure.assert_called_once_with(
        name="delete_friend", user_id=1, friend_id=2
    )


def test_delete_friend_not_friend(users, mock_db):
    mock_db.call_function.side_effect = lambda name, **kwargs: (
        1 if name == "user_exists" else
        0 if name == "is_friend" else
        None
    )
    with pytest.raises(Exception):
        users.delete_friend(1, 2)


def test_delete_friend_same_user(users, mock_db):
    with pytest.raises(Exception):
        users.delete_friend(1, 1)


def test_call_function_exception(users, mock_db):
    mock_db.call_function.side_effect = Exception("DB error")
    with pytest.raises(Exception):
        users.get_email_from_username_or_email("user1")


def test_call_procedure_exception(users, mock_db):
    mock_db.call_function.return_value = 0
    mock_db.call_procedure.side_effect = Exception("Procedure error")
    with pytest.raises(Exception):
        users.create_user(CreateUser(
            username="erroruser",
            password="pwd",
            url_avatar="avatar",
            last_name="x",
            first_name="y",
            email="x@y.com",
            is_admin=False
        ))
