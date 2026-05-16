from app.auth import create_access_token, decode_access_token


def test_token_valid():
    token = create_access_token({"sub": "1", "username": "alice"})
    payload = decode_access_token(token)
    assert payload is not None
    assert payload["sub"] == "1"
    assert payload["username"] == "alice"


def test_token_malformed():
    payload = decode_access_token("not-a-valid-token")
    assert payload is None
