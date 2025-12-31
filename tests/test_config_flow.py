import pytest

pytest.importorskip("homeassistant")

from homeassistant.const import CONF_API_KEY
from homeassistant.data_entry_flow import FlowResultType

from custom_components.govee_ble_lights.config_flow import GoveeConfigFlow
from custom_components.govee_ble_lights.const import CONF_TYPE, CONF_TYPE_API


def test_config_flow_loads_available_models():
    flow = GoveeConfigFlow()
    assert "H6053" in flow._available_models


@pytest.mark.asyncio
async def test_user_step_routes_to_api(hass):
    flow = GoveeConfigFlow()
    flow.hass = hass

    result = await flow.async_step_user({CONF_TYPE: CONF_TYPE_API})
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "api"

    result = await flow.async_step_api({CONF_API_KEY: "token"})
    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["data"] == {CONF_API_KEY: "token"}
