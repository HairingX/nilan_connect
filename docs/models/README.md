# Controller documentation

The manufacturers' documents for the controllers this library supports, each with a
machine-readable extract. **The PDF is the authority**; the extracts are working copies for
implementers and agents. Every extracted row carries the PDF page it came from.

All documents were downloaded on 2026-09-27 from the manufacturers' own sites.

| Folder | Document | Version | Source |
|---|---|---|---|
| `nilan-cts400/` | `cts400-modbus.pdf` - Protocol description, Nilan CTS400 Modbus | Modbus version 1.0, doc. version 1.10, 22-08-2024 | [nilan.dk](https://www.en.nilan.dk/Files/Files/Engelsk/Downloads/7.%20Modbus%20-%20BACnet/Modbus%20Protocol%20description%20-%20CTS400_GB.pdf) |
| `nilan-cts400/` | `cts400-software-instructions.pdf` - Software instructions, Comfort CTS400 (S75) | 1.30, 20.01.2025 | [nilan.dk](https://www.en.nilan.dk/Files/Files/Engelsk/Downloads/4.%20Software%20instructions/S75%20Comfort%20GB.pdf) |
| `nilan-cts602/` | `cts602-modbus.pdf` - CTS 602 Modbus user manual | 3.00, 19-10-2016, software 2.35 | [nilan.dk](https://www.en.nilan.dk/Files/Files/Engelsk/Archive/Software%20instructions/2016-02%20CTS602_Modbus_protokol.pdf) |
| `nilan-cts602-light/` | `cts602-light-modbus.pdf` - Protocol description, Nilan CTS602Light Modbus | Modbus version 20, revision 19.03.2019 | [nilan.dk](https://www.nilan.dk/Files/Files/Dansk/Downloads/7.%20Modbus%20-%20BACnet/2019_03_Modbus_CTS602Light_Modbus.pdf) |
| `nilan-cts602-hmi350t/` | `cts602-hmi350t-modbus.pdf` - Protocol description, Nilan CTS602 with HMI350T Modbus | Modbus version 23, revision 22.11.2023 | [nilan.dk](https://www.en.nilan.dk/Files/Files/Engelsk/Downloads/7.%20Modbus%20-%20BACnet/CTS602_w_HMI350T_Modbus.pdf) |
| `genvex-optima/` | `optima-250-user-manual.pdf` | 22.08.2014, display 3.1, PCB ES960C | [genvex.com](https://www.genvex.com/download/18.6637713118aab92aabb683/1695212792909/Operating-instructions-Optima-250-DESIGN.pdf) |
| `genvex-optima/` | `optima-251-user-manual.pdf` | PDF created 2021-04-14 | [genvex.com](https://www.genvex.com/download/18.6637713118aab92aabb623/1695212151674/Operating-instructions-Optima-251.pdf) |
| `genvex-optima/` | `optima-260-betjeningsvejledning-da.pdf` (Danish; no English edition found) | PDF created 2021-04-14 | [genvex.com](https://www.genvex.com/download/18.6637713118aab92aabb539/1695211154107/Betjeningsvejledning-Optima-260.pdf) |
| `genvex-optima/` | `optima-270-user-manual.pdf` | SW 1.5, PDF created 2026-02-10 | [genvex.com](https://www.genvex.com/download/18.2632f14918aa7daec381f25/1695212156867/Optima-270-operating-instructions.pdf) |
| `genvex-optima/` | `optima-312-user-manual.pdf` | ES960C, PDF created 2025-11-21 | [genvex.com](https://www.genvex.com/download/18.6637713118aab92aabb631/1695212256870/User-manual-Optima-312.pdf) |
| `genvex-optima/` | `optima-314-user-manual.pdf` | SW 1.4, PDF created 2026-09-24 | [genvex.com](https://www.genvex.com/download/18.309f490418b4cd507eb39a1/1763719795924/User-manual-Optima-314.pdf) |

Not found:
- **No Genvex Optima Modbus register list is published.** The user manuals refer to "a separate
  description" for Modbus; it is on none of Genvex's download pages. The user manuals are kept
  for their menus, setting ranges and sensor names.
- **Optima 301**: the user manual's download link on genvex.com answered 404 on 2026-09-27.

## Extracts

| File | Content |
|---|---|
| `*/registers.csv` | Every register in the Modbus document, one row each. |
| `nilan-cts602/alarms.csv` | The alarm codes, pages 15-16. |
| `nilan-cts400/alarms.csv` | The alarm codes of the software instructions, pages 23-24, transcribed from the text layer: the list is laid out as text, not a table. |
| `*.txt` | The text layer of the user manuals and software instructions, for searching. Diagrams leave stray characters in it. |

`registers.csv` columns: `table` (`IR` input register, function code 04; `HR` holding register,
function code 03), `address`, `name`, `unit`, `scale` (the value is register / scale),
`decimals` (the value is register / 10^decimals), `default`, `min`, `max` (in register units),
`data_type`, `plants` (the plant types a register applies to), `description`, `page`. A column
the document does not have is empty.

`extract.py` regenerates the register and CTS602 alarm extracts (`pip install pdfplumber`; it
also runs `pdftotext` from Poppler):

```
python extract.py nilan-cts400/cts400-modbus.pdf nilan-cts400/registers.csv 5
python extract.py nilan-cts602/cts602-modbus.pdf nilan-cts602/registers.csv 4
python extract.py alarms nilan-cts602/cts602-modbus.pdf nilan-cts602/alarms.csv 15 16
python extract.py nilan-cts602-light/cts602-light-modbus.pdf nilan-cts602-light/registers.csv 5
python extract.py nilan-cts602-hmi350t/cts602-hmi350t-modbus.pdf nilan-cts602-hmi350t/registers.csv 6
```

It reads the tables with pdfplumber, recovers the registers a table loses at a page break from
`pdftotext -layout`, and reports any register name in the text layer that no row carries. A
description that wraps across a table's rows can come out shortened; the page column leads to
the full text.

## What the documents say that is easy to miss

**CTS400**
- Sensors (software instructions, page 9): T1 outdoor air, T2 supply air (not in all units), T3
  extract air, T4 discharge air, T7 supply air after the after-heating element (if one is
  installed), RH% humidity in the extract air.
- Every register is 16 bit. Signed are the temperatures (input registers 27-30 and 45,
  holding registers 37-40, 45, 57 and 58) and holding register 46; all others are unsigned.
- Two holding registers are printed with contradicting options: address 46 "Fire thermostat reset
  (1=Manual / 1=Automatic)" and address 70 "Stop of unit (1=Stop/1=Operation)".
- Input register 64 is "Average level humidity 24 hours OK" and 77 "Timer used filter", the
  latter without a unit.

**CTS602 (all three documents)**
- Addresses are given without the global offset: input register 100 is global address 30101
  (function code 04), holding registers are 40001-49999. Every input register can also be read as
  a holding register at its address + 10000 (function code 03); writes there are refused.
  (`cts602-modbus.pdf`, page 3.)
- Registers carry a `Group.Name` identifier, and the register groups are laid out in blocks of
  100 (0 device, 100 discrete I/O, 200 analog I/O, 300 time, 400 alarm, ...).
- The HMI350T document is a separate line: its revision history says it was broken out of CTS602
  software 2.38o and lists only the registers implemented with the HMI350T panel.
