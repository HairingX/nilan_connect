# Nilan Connect

An event-driven Python client for **Nilan** ventilation units behind a Nilan gateway, over the
gateway's local micro_nabto protocol, built on
[modbus_event_connect](https://github.com/HairingX/modbus_event_connect).

You subscribe to the values you care about and are told when one changes - with its quality, so
"offline", "no reading" and a real value never look alike.

## Supported controllers

| Controller | Status |
|---|---|
| Nilan CTS400 | Every point checked against Nilan's Modbus manual and read from a unit |

Other controllers behind a Nilan or Genvex gateway follow. Until then, `connect()` raises
`UnsupportedDeviceError` for them.

## Installation

```bash
pip install nilan-connect
```

Everything you use comes from `nilan_connect`: the client and its values, the errors, discovery,
and, in `nilan_connect.testing`, a simulated gateway for your own tests. modbus_event_connect is
installed with it; nothing needs importing from it.

## Usage

```python
import asyncio
from nilan_connect import PointKey, create_client

def on_change(key, old, new):
    print(f"{key}: {new.value} ({new.quality.name})")

async def main():
    # The email is the account the gateway is paired with in Nilan's app.
    client = create_client("you@example.com", host="<gateway-ip>")
    await client.connect()              # reads the handshake and chooses the controller's model

    client.subscribe(PointKey.TEMP_OUTSIDE, on_change)
    client.subscribe(PointKey.FILTER_OK, on_change)

    while True:                         # you own the clock; the library owns the plan
        await client.poll()             # reads only what is due - free when nothing is
        await asyncio.sleep(1)

asyncio.run(main())
```

With only a `device_id`, the gateway is found by discovery. `discover()` lists the gateways that
answer. `port` reaches a gateway that does not answer on micro_nabto's standard port.

## How often values are read

The controller's readings every 10 seconds, its settings every 180 seconds, and a setting again
one second after it is written. A filter reset has the filter's status and timers, and the alarm
status, read again two seconds after it.

## Writing

```python
await client.write(PointKey.TEMP_TARGET, 21.5)
await client.write(PointKey.FILTER_REPLACE_RESET, True)   # an action: nothing to read back
```

A value outside the limits Nilan's manual gives is refused before anything is sent.
`create_client(..., read_only=True)` refuses every write.

## Keys

A key is the stable name of a point, and carries the type of its value. A key string never
changes, so what a consumer builds on it keeps working.

CTS400 (IR = input register, read as a datapoint; HR = holding register, read and written as a
setpoint):

| Key | Type | Register | Access | Unit | Limits |
|---|---|---|---|---|---|
| `bypass_active` | bool | IR 23 | read |  |  |
| `fan_dutycycle_extract` | float | IR 24 | read | % |  |
| `fan_dutycycle_supply` | float | IR 25 | read | % |  |
| `temp_outside` | float | IR 27 | read | °C |  |
| `temp_supply` | float | IR 28 | read | °C |  |
| `temp_extract` | float | IR 29 | read | °C |  |
| `temp_exhaust` | float | IR 30 | read | °C |  |
| `humidity` | float | IR 31 | read | % |  |
| `humidity_average` | float | IR 46 | read | % |  |
| `co2_level` | int | IR 47 | read | ppm |  |
| `voc_level` | int | IR 48 | read | ppm |  |
| `filter_ok` | bool | IR 49 | read |  |  |
| `alarm_status` | bool | IR 50 | read |  |  |
| `alarm_1_code` | int | IR 51 | read |  |  |
| `alarm_2_code` | int | IR 52 | read |  |  |
| `alarm_3_code` | int | IR 53 | read |  |  |
| `alarm_1_info` | int | IR 56 | read |  |  |
| `alarm_2_info` | int | IR 57 | read |  |  |
| `alarm_3_info` | int | IR 58 | read |  |  |
| `fan_level_current` | int | IR 63 | read |  |  |
| `humidity_high_active` | bool | IR 64 | read |  |  |
| `humidity_high_level` | float | IR 66 | read |  |  |
| `humidity_high_level_time` | float | IR 70 | read | min |  |
| `winter_mode_active` | bool | IR 72 | read |  |  |
| `filter_replace_time_ago` | float | IR 77 | read | d |  |
| `defrost_active` | bool | IR 91 | read |  |  |
| `filter_replace_time_remain` | int | IR 110 | read | d |  |
| `alarm_reset` | bool | HR 30 | write |  |  |
| `humidity_low_threshold` | float | HR 31 | read, write | % | 15–45 |
| `fan_level_low_humidity` | int | HR 32 | read, write |  | 0–3 |
| `fan_level_high_humidity` | int | HR 33 | read, write |  | 2–4 |
| `fan_level_high_humidity_time` | int | HR 34 | read, write | min | 0–180 |
| `co2_threshold` | int | HR 35 | read, write | ppm | 500–2000 |
| `voc_threshold` | int | HR 36 | read, write | ppm | 500–2000 |
| `temp_target` | float | HR 37 | read, write | °C | 10–30 |
| `temp_regulation_dead_band` | float | HR 38 | read, write | °C | 0–4 |
| `temp_defrost_low_threshold` | float | HR 39 | read, write | °C | 1–5 |
| `temp_defrost_high_threshold` | float | HR 40 | read, write | °C | 5–10 |
| `defrost_max_time` | int | HR 41 | read, write | min | 5–60 |
| `defrost_break_time` | int | HR 43 | read, write | min | 15–760 |
| `temp_winter_mode_threshold` | float | HR 45 | read, write | °C | 5–20 |
| `filter_replace_interval` | int | HR 50 | read, write | d | 0–360 |
| `filter_replace_reset` | bool | HR 51 | write |  |  |
| `temp_supply_min` | float | HR 57 | read, write | °C | 10–20 |
| `temp_supply_max` | float | HR 58 | read, write | °C | 10–50 |
| `fan_level1_supply_preset` | float | HR 59 | read, write | % | 20–100 |
| `fan_level2_supply_preset` | float | HR 60 | read, write | % | 20–100 |
| `fan_level3_supply_preset` | float | HR 61 | read, write | % | 20–100 |
| `fan_level4_supply_preset` | float | HR 62 | read, write | % | 20–100 |
| `fan_level1_extract_preset` | float | HR 63 | read, write | % | 20–100 |
| `fan_level2_extract_preset` | float | HR 64 | read, write | % | 20–100 |
| `fan_level3_extract_preset` | float | HR 65 | read, write | % | 20–100 |
| `fan_level4_extract_preset` | float | HR 66 | read, write | % | 20–100 |
| `fan_level` | int | HR 69 | read, write |  | 1–4 |
| `enable` | bool | HR 70 | read, write |  |  |
| `fan_level_high_co2` | int | HR 80 | read, write |  | 2–4 |

`filter_ok` is the manual's "filter change status" the other way round, and
`humidity_high_active` its "average level humidity 24 hours OK" the other way round.

## Documentation

[docs/models](https://github.com/HairingX/nilan_connect/tree/main/docs/models) holds the
manufacturers' manuals for every controller, with every register extracted to CSV.

## A note to Nilan

Thank you for publishing the Modbus descriptions of your controllers, and for gateways that
answer on their owner's own network. They are what lets an owner fit a Nilan unit into a home
the way they want it.

We know a gateway can be updated remotely, and that its local access could be closed. Please
keep it open. A local connection needs the email the gateway is paired with in your app, and it
reaches the same values your Modbus descriptions give anyone who wires to the controller
directly: it adds nothing Modbus does not already allow, and it makes your gateway worth more to
the people who own one.

## Disclaimer

Not affiliated with Nilan or Genvex. Use at your own risk; no warranty.

## License

MIT. See [LICENSE](https://github.com/HairingX/nilan_connect/blob/main/LICENSE).
