# Nilan Connect

An event-driven Python client for **Nilan** and **Genvex** ventilation units behind their
gateway, over the gateway's local micro_nabto protocol, built on
[modbus_event_connect](https://github.com/HairingX/modbus_event_connect).

You subscribe to the values you care about and are told when one changes - with its quality, so
"offline", "no reading" and a real value never look alike.

## Supported controllers

| Controller | Status |
|---|---|
| Nilan CTS400 | Tested: every point checked against Nilan's Modbus manual and read from a unit |
| Genvex Optima 270 | Tested: read from a unit |
| Nilan CTS602, every variant including Geo | Untested, apart from four temperatures (T2, T3, T4, T8) read from a unit |
| Nilan CTS602 Light | Untested |
| Genvex Optima 250, 251, 260, 301, 312, 314 | Untested |

**The gateway's addresses of the untested controllers are derived and calculated from the
material we could find online, and have not been tested on those controllers.** Values may be
wrong or missing; reports of what a unit shows are welcome. `connect()` raises
`UnsupportedDeviceError` for any other controller.

A point's `certainty` says how certain it is that the point is right:

| `Certainty` | Meaning |
|---|---|
| `VERIFIED` | Read on a unit of the model. |
| `REPORTED` | Found in material published online; not read on a unit of the model. |
| `INFERRED` | Placed from the model's Modbus manual by the order of its register group; not read on a unit of the model, and not found elsewhere. |

On a CTS602 the gateway does not use the manual's addresses. Within one of the manual's register
groups - blocks of 100, such as the temperatures from input register 200 - it keeps the manual's
order and spacing, so a group's other registers follow from one known address in it: those are
the `inferred` points. A setting among them can be written, as a test of it needs to.

### Levels and candidates

A client uses the points of its `level`, chosen when it is made:

| `Level` | The points a client has |
|---|---|
| `VERIFIED` | Only `VERIFIED` points. |
| `DOCUMENTED` (the default) | `VERIFIED` and `REPORTED` points. |
| `TEST` | Every point, `INFERRED` ones included, and each candidate in place of the point it replaces. |

A **candidate** is a point read on no unit of the model yet, whose place a source gives: it is
used only at `TEST`, so that the owner of such a unit can compare its values with the unit's
panel. Below `TEST` the model is exactly as without it. `point.candidate` says a point is one,
and `point.candidate.replaces` the key of the point it takes the place of, or None for a point
of its own. Where it replaces a point of the same key, a consumer that stores the key keeps it;
only the register behind it changes. A candidate that is confirmed on a unit becomes a point
like any other, and its source is named on its line in the model.

| Controller | Candidate | Replaces | Source |
|---|---|---|---|
| Optima 250, 251 | `bypass_active` at datapoint 107, "Bypass ON/OFF" | `bypass_active` at datapoint 104, the bypass's opening, 0-100 % | Genvex's register workbook |
| Optima 301 | `preheat_enable` at setpoint 16, "Preheat (on/off)" | - | Genvex's register workbook |
| Optima 301 | `min_air_volume` at setpoint 20, "Min air volume (%)" | - | Genvex's register workbook; the Optima 312's user manual, item 24 |

Genvex's register workbook was posted on the
[OpenEnergyMonitor forum](https://community.openenergymonitor.org/t/reverse-engineer-heatpump-genvex-combi-185/15992/46).

```python
from nilan_connect import Level, create_client

client = create_client(email="you@example.com", host="192.0.2.10", level=Level.TEST)
```

`client.diagnostics()` names the level, the certainty of each point and the candidates in use.
`model_points(model)` gives every point a model declares, whatever the unit and the level: of each
variant, with its certainty, and each candidate beside the point it replaces.

## Installation

```bash
pip install nilan-connect
```

Everything you use comes from `nilan_connect`: the client and its values, the errors, discovery,
and, in `nilan_connect.testing`, a simulated gateway and a client of it for your own tests.
modbus_event_connect is installed with it; nothing needs importing from it. The client is the
`DeviceClient` every device library built on event_connect shares, and the names they share
(`Status`, `Quality`, `PollRate`, the errors, ...) are event_connect's own.

## Usage

```python
import asyncio
from nilan_connect import PointKey, create_client

def on_change(key, old, new):
    print(f"{key}: {new.value} ({new.quality.name})")

async def main():
    # The email is the account the gateway is paired with in Nilan's app.
    client = create_client(email="you@example.com", host="192.0.2.10")
    await client.connect()              # reads the handshake and chooses the controller's model

    client.subscribe(PointKey.TEMP_OUTSIDE, on_change)
    client.subscribe(PointKey.FILTER_OK, on_change)

    await client.run()                  # reads whatever is due, until cancelled

asyncio.run(main())
```

`create_client` takes keyword arguments only: `email`, `host`, `device_id`, `port` (micro_nabto's
standard `PORT` unless given), `level` (`Level.DOCUMENTED` unless given), `read_only` and
`clock`. With only a `device_id`, the gateway is found by discovery, and with both, a gateway
that has moved is found again. `run()` is the whole poll loop, and never ends by itself: it
waits while the client is not connected, and logs a poll that raises and polls on after a pause.
A program with a loop of its own calls `poll()`, which reads only what is due, and waits
`seconds_until_next_poll()`.

```python
from nilan_connect import discover

async def find():
    for gateway in await discover():                # every gateway on the local network
        print(gateway.host, gateway.port, gateway.device_id)
    return await discover(target="192.0.2.10")      # the gateway at one address
```

Discovery waits two seconds for answers.

## Mapping a unit

To find out what a controller's registers mean, its owner changes one thing at a time on the
unit's own panel, and the registers are read as raw words before and after each change:

```python
from nilan_connect import difference

async def map_unit(client):
    found = await client.map_areas(limit=300)   # every address 0-299: its word, or missing
    input("Change one thing on the panel, then press Enter")
    after = await client.read_mapped(found)     # only the registers found
    for change in difference(found, after):
        print(change.address, change.before, change.after, change.bits)
```

The registers are the gateway's own datapoints and setpoints, never the manuals' Modbus numbers:
every address from 0 up to the `limit`, or up to the highest the controller's model reads or
writes where that is higher, ends with its word or as missing; none is skipped. The first read
finds which registers the gateway has: on a CTS400 with a limit of 300 about 670 requests, as
each absent address is asked for alone, which takes seconds on a quick gateway and up to a few
minutes on a slow one. Each read after it reads only the registers found, in two requests.
Nothing is read for a mapping unless it is asked for, and nothing is written.
`tools/measure_mapping.py` measures, read-only, how far a gateway's numbering goes.

## How often values are read

Each controller's model says when its points are read, and nothing outside the model or
`create_client` changes it. Every model reads the controller's readings every 10 seconds, its
settings every 180 seconds, and a setting again one second after it is written. What a write
changes is read again too: after a filter reset on a CTS400, the filter's status and timers and
the alarm status, two seconds later; after a filter interval, the days left, two seconds later;
after a fan level, on every controller, the levels the fans run at and their speeds, three
seconds later. The setting itself is read back after one second either way. A CTS400 is checked
every 900 seconds for whether a CO2 or VOC sensor has been fitted or taken out.

Only what is subscribed to, or asked for with `refresh()`, is read.

## The gateway

The gateway is a device of its own between the network and the controller. It reaches the
controller over RS-485 Modbus at 19,200 baud, as the master, and gives the controller's registers
addresses of its own.

**It answers from what it holds, not from the controller.** A CTS602's gateway answered reads of
4 to 31 registers within 7 to 24 ms, the trip over the network included. Asked of the controller
over RS-485, one register alone takes about 13 ms, and those reads, which span up to five of the
manual's register groups, at least 40 to 95 ms.

What is known of a gateway was seen on the gateway of one controller or another, and is named
with it here; whether the others' gateways behave alike is not known. Each controller's model
states how its gateway is talked to: where nothing was seen on that controller's gateway, with
what was seen on another's, or a guess.

A gateway counts as not answering once it has left reads unanswered for 10 seconds: one missed
read keeps the last values, and a gateway that stays silent shows as not answering. After a
failed handshake it is asked again after 5 seconds, before the next read is due. A read the
gateway has said it has is given 2 seconds to be answered, a write or a first handshake 5
seconds: a CTS602's gateway answered 21,000 reads within 245 ms.

What it holds can be empty. A CTS602's gateway answered the first reads of a new session with
only zeros, at once and again 18 ms later, and with values 10 s later. The same gateway was
reported leaving a read unanswered every 33 minutes and answering the next. Not known yet:

- whether it empties what it holds when a session begins, when it restarts, or at some interval;
- how long it takes to fill it;
- whether every controller's gateway works this way: only a CTS602's has been measured.

modbus_event_connect handles such an answer for any device, also one read directly: the last
values are kept while the registers are read again, and the zeros are taken if they stay. It logs,
as warnings, why each session began, when the gateway went silent and answered again, and how long
it took to answer values. Those lines answer the questions above; please include them in a report.

## Writing

```python
await client.write(PointKey.TEMP_TARGET, 21.5)
await client.write(PointKey.FILTER_REPLACE_RESET, True)   # an action: nothing to read back
```

A value outside the limits Nilan's manual gives is refused before anything is sent.
`create_client(..., read_only=True)` refuses every write.

The gateway answers a write with a status. A CTS400's gateway answered 0 to a write it took; an
Optima 270's gateway answered 0x01 to every write it took, so its model takes either as taken.
An Optima 314 takes either too, a guess: its gateway is built in as the Optima 270's is. The
other models take 0 alone, a guess. A CTS400's gateway answered some writes with a status
saying it did not take them, and took the same write on a later try. A write answered with a
status its model does not take is sent again every half second, for up to 15 seconds after it was
first sent; every model does so, as nothing else is known. A newer value for the same setting
takes over from it.

## How each controller is talked to

Each model is a `MicroNabtoModel` in a file of its own, read top to bottom: its points, when they
are read, and how its gateway is talked to, each number with where it comes from. `MODELS` lists
them all, and `select_model` chooses one from the gateway's handshake. Every model asks its
gateway for at most 64 registers in one read. A read sent again, as its receipt did not come, and
answered with only zeros where the registers held values, is kept open for a later answer: 1 s
for a CTS400, the 1 s a request is given before it is sent again, and 5 s for the other
controllers, on which it has not been measured. Until the controller's model is known, the
longest of them is used.

## Keys

A key is the stable name of a point, and carries the type of its value. A key string never
changes, so what a consumer builds on it keeps working.

Every key is in `PointKey`. Which keys a controller has, and at which registers, is its model's:
`client.points` lists the points of the unit connected, each with its unit, limits and whether
it is read, written or both.

`filter_ok` is the CTS400 manual's "filter change status" the other way round, and
`humidity_high_active` is whether its "time of high humidity" counts. Its "average level
humidity 24 hours OK" is `humidity_average_ok`.

Controllers share a key wherever a value means the same.

## States

A value with named states is an `IntEnum`, one for all controllers: `Alarm`, `OperationState`,
`OperationMode`, `Weekday`, `HeatSource`, `CompressorPriority`, `CoolingSetpoint`,
`AirExchangeMode`, `ControlSensor`, `CentralHeatMode`, `CirculationPumpMode`, `ServiceMode`,
`DamperTestState`, `FilterReplaceInterval` and `ExtraSensor`. Each controller maps its own numbers onto them, so a state means the same
whichever controller reports it: a CTS400's alarm 1 and a CTS602's alarm 19 are both
`Alarm.CHANGE_FILTER`.

- A key ending in `_code` holds the controller's own number. What it means is a key of its own:
  `alarm_1` for `alarm_1_code`, `operation_state` for `state_code`.
- An Optima reports its alarms as bits. Each is a `bool` key named after its alarm, such as
  `alarm_external_stop`; its filter alarm is `filter_ok`, the other way round.
- A sensor alarm names the sensor by the controller's T number, as the controller's panel does.
- When an alarm was raised (`alarm_1_time`) and when the damper last tested itself
  (`damper_test_last_date`) are in the controller's own clock, without a time zone.

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
