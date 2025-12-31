from types import SimpleNamespace

import pytest

pytest.importorskip("homeassistant")

from custom_components.govee_ble_lights import Hub
from custom_components.govee_ble_lights.light import GoveeBluetoothLight, LedCommand


@pytest.mark.parametrize(
    "cmd,payload",
    [
        ("bad", [0x01]),
        (LedCommand.POWER, "bad"),
        (LedCommand.POWER, list(range(20))),
    ],
)
def test_prepare_single_packet_data_validates_inputs(cmd, payload):
    hub = Hub(api=None, address="AA:BB:CC:DD:EE:FF")
    config_entry = SimpleNamespace(data={"model": "H6102"})
    light = GoveeBluetoothLight(hub, ble_device=None, config_entry=config_entry)

    with pytest.raises(ValueError):
        light._prepareSinglePacketData(cmd, payload)


def test_prepare_single_packet_data_builds_frame_with_checksum():
    hub = Hub(api=None, address="AA:BB:CC:DD:EE:FF")
    config_entry = SimpleNamespace(data={"model": "H6102"})
    light = GoveeBluetoothLight(hub, ble_device=None, config_entry=config_entry)

    frame = light._prepareSinglePacketData(LedCommand.POWER, [0x01])

    assert len(frame) == 20
    assert frame[0] == 0x33
    assert frame[1] == LedCommand.POWER
    assert frame[2] == 0x01

    checksum = 0
    for b in frame[:-1]:
        checksum ^= b
    assert frame[-1] == (checksum & 0xFF)
