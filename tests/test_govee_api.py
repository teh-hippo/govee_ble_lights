import pytest
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

pytest.importorskip("requests")

spec = spec_from_file_location(
    "govee_api",
    Path(__file__).resolve().parents[1]
    / "custom_components"
    / "govee_ble_lights"
    / "govee_api.py",
)
govee_api = module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(govee_api)
GoveeAPI = govee_api.GoveeAPI


class DummyResponse:
    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload


@pytest.mark.asyncio
async def test_list_devices_uses_expected_url_and_headers(monkeypatch):
    captured = {}

    def fake_get(url, headers=None):
        captured["url"] = url
        captured["headers"] = headers
        return DummyResponse({"data": [{"device": "AA"}]})

    monkeypatch.setattr(govee_api.requests, "get", fake_get)

    api = GoveeAPI("api-key")
    devices = await api.list_devices()

    assert devices == [{"device": "AA"}]
    assert captured["url"].endswith("/user/devices")
    assert captured["headers"]["Govee-API-Key"] == "api-key"


@pytest.mark.asyncio
async def test_set_color_rgb_sends_expected_payload(monkeypatch):
    captured = {}

    def fake_post(url, headers=None, json=None):
        captured["url"] = url
        captured["headers"] = headers
        captured["json"] = json
        return DummyResponse({"ok": True})

    monkeypatch.setattr(govee_api.requests, "post", fake_post)

    api = GoveeAPI("api-key")
    response = await api.set_color_rgb("SKU", "DEV", 1, 2, 3)

    assert response == {"ok": True}
    assert captured["url"].endswith("/device/control")
    assert captured["headers"]["Govee-API-Key"] == "api-key"
    payload = captured["json"]["payload"]["capability"]
    assert payload["type"] == "devices.capabilities.color_setting"
    assert payload["instance"] == "colorRgb"
    assert payload["value"] == (1 << 16) | (2 << 8) | 3
