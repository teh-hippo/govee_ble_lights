from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

pytest.importorskip("homeassistant")

from homeassistant.components.light import ATTR_EFFECT
from homeassistant.helpers.storage import Store

from custom_components.govee_ble_lights import Hub
from custom_components.govee_ble_lights.const import DOMAIN
from custom_components.govee_ble_lights.light import GoveeAPILight


@pytest.mark.asyncio
async def test_api_light_turn_on_sets_effect_from_store(hass, monkeypatch):
    monkeypatch.setattr(GoveeAPILight, "update_scenes", lambda self: None)

    api = SimpleNamespace(
        set_scene=AsyncMock(),
        toggle_power=AsyncMock(),
        set_brightness=AsyncMock(),
        set_color_rgb=AsyncMock(),
        set_color_temp=AsyncMock(),
    )
    hub = Hub(api=api)

    device = {
        "device": "DEV",
        "deviceName": "Lamp",
        "sku": "SKU",
        "type": "devices.types.light",
        "capabilities": [
            {"instance": "powerSwitch"},
            {"instance": "lightScene"},
        ],
    }

    entity = GoveeAPILight(hub, device)
    entity.hass = hass

    store = Store(hass, 1, f"{DOMAIN}/effect_list_{device['sku']}.json")
    await store.async_save([
        {"name": "Rainbow", "value": {"scene": 1}},
        {"name": "Pulse", "value": {"scene": 2}},
    ])

    await entity.async_turn_on(**{ATTR_EFFECT: "Pulse"})

    api.set_scene.assert_awaited_once_with("SKU", "DEV", {"scene": 2})
    api.toggle_power.assert_awaited_once_with("SKU", "DEV", 1)
