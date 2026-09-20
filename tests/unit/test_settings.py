from app.infrastructure.config.settings import get_settings


def test_settings_load():
    settings = get_settings()

    assert settings.app_name == "Learning Advisor"
    assert settings.environment == "development"
    assert settings.qdrant_url == "http://localhost:6333"