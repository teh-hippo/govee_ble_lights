import pytest

pytest.importorskip("homeassistant")

from custom_components.govee_ble_lights import __init__ as govee_init


def test_internal_unique_devices_filters_duplicate_devices(monkeypatch):
    monkeypatch.setattr(govee_init, "UNIQUE_DEVICES", {})
    devices = [
        {"device": "AA:BB:CC"},
        {"device": "DD:EE:FF"},
        {"device": "AA:BB:CC"},
    ]

    first = govee_init.internal_unique_devices("uid-1", devices)
    assert first == devices[:2]

    second = govee_init.internal_unique_devices("uid-2", devices)
    assert second == []
