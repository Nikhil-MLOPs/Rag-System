def test_api_app_imports():
    from src.api.app import app
    assert app is not None