"""Extract the register tables of a Nilan Modbus PDF into one CSV row per register.

Usage: python extract.py MANUAL.pdf REGISTERS.csv FIRST_REGISTER_PAGE
       python extract.py alarms MANUAL.pdf ALARMS.csv PAGE [PAGE ...]

Tables are read with pdfplumber. A register the table finder loses at a page break is read
from pdftotext's layout text instead, and the result is checked against every register name
the text layer holds.
"""
import csv
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import pdfplumber
from pdfplumber.page import Page

LABELS = {
    "name": "name", "address": "address", "addres": "address", "modbus address": "address",
    "scale": "scale", "scal": "scale", "unit": "unit", "description": "description",
    "used to plant type": "plants", "factory reset": "default", "min.": "min", "max.": "max",
    "number of decimals": "decimals", "data type": "data_type",
}
COLUMNS = ["table", "address", "name", "unit", "scale", "decimals", "default", "min", "max",
           "data_type", "plants", "description", "page"]
HEADING = re.compile(r"^(\d+(\.\d+)*\.?\s*)?(Modbus \w+ for .*\()?(Input|Holding) registers?\)?:?\s*$", re.I)
REGISTER_LINE = re.compile(r"^\s*([A-Z]\w*\.\w+)\s{2,}(\d{1,4})\s{2,}(.*)$")
FORM_FEED = "\f"


def clean(cell: str | None) -> str:
    return re.sub(r"\s+", " ", (cell or "").replace("�", "°")).strip()


def header_of(row: list[str]) -> dict[int, str] | None:
    found = {i: LABELS[c.lower()] for i, c in enumerate(row) if c.lower() in LABELS}
    return found if "name" in found.values() and "address" in found.values() else None


def assign(row: list[str], header: dict[int, str]) -> dict[str, str]:
    """Give each cell to the nearest header label at or right of its column."""
    positions = sorted(header)
    record: dict[str, str] = {}
    for column, cell in enumerate(row):
        if not cell:
            continue
        field = header[next((p for p in positions if p >= column), positions[-1])]
        record[field] = f"{record[field]} {cell}".strip() if field in record else cell
    return record


def tidy(record: dict[str, str]) -> dict[str, str]:
    if "." in record.get("name", ""):
        record["name"] = re.sub(r"[^\w.].*$", "", record["name"].replace(" ", ""))
    if "plants" in record:
        record["plants"] = record["plants"].replace("A ll", "All").replace("- ", "-")
    record["address"] = str(int(record["address"]))
    return record


def beside(page: Page, row: tuple[float, float, float, float], right: float) -> str:
    """The words right of a table within one of its rows: a column drawn without borders,
    which the table finder leaves out."""
    words: list[dict[str, Any]] = page.extract_words()
    return clean(" ".join(str(w["text"]) for w in words
                          if w["x0"] >= right and row[1] <= w["top"] and w["bottom"] <= row[3]))


def from_tables(pdf_path: Path, first_page: int) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    kind = ""
    header: dict[int, str] | None = None
    with pdfplumber.open(pdf_path) as pdf:
        for number, page in enumerate(pdf.pages, 1):
            if number < first_page:
                continue
            headings = [(line["top"], "IR" if "input" in line["text"].lower() else "HR")
                        for line in page.extract_text_lines() if HEADING.match(line["text"].strip())]
            for table in page.find_tables():
                for heading_top, heading_kind in headings:
                    if heading_top < table.bbox[1]:
                        kind = heading_kind
                data = [[clean(c) for c in r] for r in table.extract()]
                extra = [beside(page, row.bbox, table.bbox[2]) for row in table.rows]
                if data and extra[0].lower() in LABELS:
                    data = [r + [e] for r, e in zip(data, extra)]
                if not data or len(data[0]) < 4 or "VPM" in data[0]:
                    continue
                own = header_of(data[0])
                if own:
                    header, data = own, data[1:]
                elif len(data[0]) == 6:
                    header = {0: "name", 1: "address", 2: "scale", 3: "unit", 4: "description", 5: "plants"}
                else:
                    header = None
                if header is None:
                    continue
                for raw in data:
                    record = assign(raw, header)
                    if not record:
                        continue
                    if not re.fullmatch(r"\d+", record.get("address", "")):
                        if rows and set(record) <= {"description", "plants", "name", "unit"}:
                            for key, value in record.items():
                                rows[-1][key] = f"{rows[-1].get(key, '')} {value}".strip()
                        continue
                    rows.append(tidy(record | {"table": kind, "page": str(number)}))
    return rows


def layout_text(pdf_path: Path) -> list[str]:
    output = subprocess.run(["pdftotext", "-enc", "UTF-8", "-layout", str(pdf_path), "-"],
                            capture_output=True, check=True).stdout
    return output.decode("utf-8").split("\n")


def from_text(text: list[str], known: set[str]) -> list[dict[str, str]]:
    """Registers missing from the tables: name and address open a line, columns are two or
    more spaces apart, and the enumeration lines below (`n : text`) extend the description."""
    found: list[dict[str, str]] = []
    kind = ""
    page = 1
    for index, raw in enumerate(text):
        page += raw.count(FORM_FEED)
        line = raw.replace(FORM_FEED, "")
        if HEADING.match(line.strip()):
            kind = "IR" if "input" in line.lower() else "HR"
        match = REGISTER_LINE.match(line)
        if not match:
            continue
        name, address, rest = match.groups()
        wrapped = re.match(r"^(\w+)(\s{2,}|$)", text[index + 1].replace(FORM_FEED, "")) if index + 1 < len(text) else None
        if wrapped:
            name += wrapped.group(1)
        if name in known:
            continue
        fields = re.split(r"\s{2,}", rest.strip())
        record = {"name": name, "address": address, "page": str(page), "table": kind}
        if fields and fields[0].isdigit():
            record["scale"] = fields.pop(0)
        if fields and len(fields[0]) <= 4 and not fields[0][0].isdigit():
            record["unit"] = fields.pop(0)
        record["description"] = fields.pop(0) if fields else ""
        if fields:
            record["plants"] = fields.pop(0)
        for follow in text[index + 1:]:
            follow = follow.replace(FORM_FEED, "")
            if re.match(r"^\s*\d+\s*:\s*\S", follow):
                record["description"] += " " + re.sub(r"\s+", " ", follow.strip())
            elif follow.strip() and not follow.lstrip().startswith("All rights"):
                break
        found.append(tidy(record))
    return found


def unaccounted(text: list[str], rows: list[dict[str, str]]) -> list[str]:
    """Register names in the text layer that no row carries, whole or as a wrapped prefix."""
    names = {r["name"] for r in rows}
    in_text = set(re.findall(r"\b([A-Z][A-Za-z0-9]*\.[A-Za-z0-9_]+)", "\n".join(text)))
    return sorted(n for n in in_text if not any(name.startswith(n) for name in names))


def alarms(pdf_path: Path, pages: list[int]) -> list[dict[str, str]]:
    """The alarm code table: code, text, type, subsystem, function."""
    found: list[dict[str, str]] = []
    with pdfplumber.open(pdf_path) as pdf:
        for number in pages:
            for table in pdf.pages[number - 1].extract_tables():
                for raw in table:
                    cells = [c for c in (clean(c) for c in raw) if c]
                    if len(cells) < 5 or not cells[0].isdigit():
                        continue
                    code, text, kind, subsystem, function = cells[:5]
                    found.append({
                        "code": code,
                        # A word wrapped inside its cell leaves its last letter on its own: "HARDWAR E".
                        "text": re.sub(r"(\w) (\w)$", r"\1\2", text),
                        "type": re.sub(r"\s+", "", kind).replace("+", " + "),
                        "subsystem": subsystem, "function": function, "page": str(number)})
    return found


if __name__ == "__main__" and sys.argv[1] == "alarms":
    records = alarms(Path(sys.argv[2]), [int(p) for p in sys.argv[4:]])
    with Path(sys.argv[3]).open("w", newline="", encoding="utf-8") as out:
        writer = csv.DictWriter(out, ["code", "text", "type", "subsystem", "function", "page"],
                                lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)
    print(f"{sys.argv[3]}: {len(records)} alarms")
elif __name__ == "__main__":
    source, target, first = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])
    text = layout_text(source)
    records = from_tables(source, first)
    in_text = set(re.findall(r"\b([A-Z][A-Za-z0-9]*\.[A-Za-z0-9_]+)", "\n".join(text)))
    for found in from_text(text, {r["name"] for r in records}):
        same = [r for r in records if (r["table"], r["address"]) == (found["table"], found["address"])]
        if not same:
            records.append(found)
        elif same[0]["name"] not in in_text and same[0]["name"].startswith(found["name"]):
            same[0]["name"] = found["name"]  # the table cell ran into its neighbour's text
    records.sort(key=lambda r: (r["table"] != "IR", int(r["address"])))
    with target.open("w", newline="", encoding="utf-8") as out:
        writer = csv.DictWriter(out, COLUMNS, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)
    duplicates = sorted({(r["table"], r["address"]) for r in records
                         if sum((o["table"], o["address"]) == (r["table"], r["address"]) for o in records) > 1})
    print(f"{target.name}: {len(records)} registers, IR={sum(r['table'] == 'IR' for r in records)} "
          f"HR={sum(r['table'] == 'HR' for r in records)}, duplicates={duplicates}, "
          f"unaccounted={unaccounted(text, records)}")
