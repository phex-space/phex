import pytest
from phexcore import services

def test_service_register_and_get():
    services.register("test", lambda: "test value")

    assert services.get("test") is not None

def test_fail_multiple_registration():
    with pytest.raises(ValueError):
        services.register("test", lambda: "test value")

def test_fail_for_missing_service():
    with pytest.raises(ValueError):
        services.get("unknown_test")
