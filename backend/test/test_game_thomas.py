import sys
import os
from unittest.mock import MagicMock, patch
import pytest
from fastapi import HTTPException


# Ajoute le dossier backend au PYTHONPATH si besoin
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

with patch.dict('sys.modules', {
    'api.models': MagicMock(),
    'api.user': MagicMock(),
    'api': MagicMock(),
    'classes.database': MagicMock(),
    'classes.debug': MagicMock(),
    'classes.mail': MagicMock(),
}):
    from classes.users import UsersAPI

@pytest.fixture
def mock_db():
    db = MagicMock()
    db.call_function = MagicMock()
    db.call_procedure = MagicMock()
    return db

@pytest.fixture
def mock_debug():
    return MagicMock()

@pytest.fixture
def users_api(mock_db, mock_debug):
    return UsersAPI(db=mock_db, debug=mock_debug)

def test_get_opponent(users_api, mock_db):
    # Arrange
    users_api.list_members = MagicMock(return_value=[
        {"user_ID": 1, "pseudo": "User1"},
        {"user_ID": 2, "pseudo": "User2"},
        {"user_ID": 3, "pseudo": "User3"}
    ])
    mock_db.call_function.return_value = 7

    # Act
    result = users_api.get_opponent(user_id=1)

    # Assert
    assert isinstance(result, list)
    assert len(result) == 2  # On enlève l'utilisateur 1
    for user in result:
        assert user["beers"] == 7
        assert user["user_ID"] != 1
    mock_db.call_function.assert_called_with(name="get_user_beer_reserve", uid=1)

def test_do_transaction_success(users_api, mock_db, mock_debug):
    # Arrange
    users_api.check_uid = MagicMock(return_value=True)
    mock_db.call_function.side_effect = [
        1,      # has_enough_beer
        10,     # how_many_beer (loser)
        5       # how_many_beer (winner)
    ]
    mock_db.call_procedure = MagicMock()

    # Act
    result = users_api.do_transaction(winner_id=2, loser_id=1, beers=5)

    # Assert
    assert result["success"] is True
    assert result["message"] == "Transaction completed"
    mock_db.call_function.assert_any_call("has_enough_beer", uid=1, beers=5)
    mock_db.call_function.assert_any_call(name="how_many_beer", uid=1)
    mock_db.call_function.assert_any_call(name="how_many_beer", uid=2)
    mock_db.call_procedure.assert_any_call(name="do_beer_transaction", uid=1, beer=5)
    mock_db.call_procedure.assert_any_call(name="do_beer_transaction", uid=2, beer=10)
    mock_db.call_procedure.assert_any_call(name="add_transaction", looser_uid=1, winner_uid=2, beers_owed=5)

def test_do_transaction_not_enough_beers(users_api, mock_db, mock_debug):
    # Arrange
    users_api.check_uid = MagicMock(return_value=True)
    mock_db.call_function.side_effect = [
        0  # has_enough_beer
    ]

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        users_api.do_transaction(winner_id=2, loser_id=1, beers=5)
    assert exc_info.value.status_code == 405
    assert "n'a plus assez de bieres" in exc_info.value.detail
    mock_db.call_function.assert_any_call("has_enough_beer", uid=1, beers=5)