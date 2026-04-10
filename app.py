# written by AI (chatgpt 5.3 instant)
from __future__ import annotations

import sqlite3
from datetime import date
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for


DB_PATH = Path("fakeerp.db")


FAKE_DB = {
    "11023": [
        # -------------------------
        # Version 3
        # -------------------------
        {"sku": "11023", "item_grp": "0003", "item": "version_nr", "description": "3", "qty": None, "from_date": "2024-01-01", "to_date": "2024-01-31"},

        {"sku": "11023", "item_grp": "0200", "item": "550412-02", "description": "Steel plate",    "qty": 2,  "from_date": "2024-01-01", "to_date": "2024-03-31"},
        {"sku": "11023", "item_grp": "0300", "item": "660221-01", "description": "Screw M6",       "qty": 8,  "from_date": "2024-01-01", "to_date": "2024-01-31"},
        {"sku": "11023", "item_grp": "0400", "item": "770100-01", "description": "Bracket",        "qty": 1,  "from_date": "2024-01-01", "to_date": "2024-02-29"},
        {"sku": "11023", "item_grp": "0500", "item": "810500-01", "description": "Hex nut M6",     "qty": 8,  "from_date": "2024-01-01", "to_date": None},
        {"sku": "11023", "item_grp": "0600", "item": "820700-01", "description": "Spacer 10mm",    "qty": 4,  "from_date": "2024-01-01", "to_date": None},
        {"sku": "11023", "item_grp": "0700", "item": "830120-01", "description": "Mounting rail",  "qty": 2,  "from_date": "2024-01-01", "to_date": None},
        {"sku": "11023", "item_grp": "0800", "item": "840330-01", "description": "Clamp",          "qty": 2,  "from_date": "2024-01-01", "to_date": None},
        {"sku": "11023", "item_grp": "0900", "item": "850440-01", "description": "Cable tie",      "qty": 6,  "from_date": "2024-01-01", "to_date": None},
        {"sku": "11023", "item_grp": "1000", "item": "860550-01", "description": "Protective cap", "qty": 2,  "from_date": "2024-01-01", "to_date": None},
        {"sku": "11023", "item_grp": "1100", "item": "870660-01", "description": "Ground wire",    "qty": 1,  "from_date": "2024-01-01", "to_date": None},

        # -------------------------
        # Version 4
        # -------------------------
        {"sku": "11023", "item_grp": "0004", "item": "version_nr", "description": "4", "qty": None, "from_date": "2024-02-01", "to_date": "2024-02-29"},

        {"sku": "11023", "item_grp": "0300", "item": "660221-02", "description": "Screw M6", "qty": 12, "from_date": "2024-02-01", "to_date": None},
        {"sku": "11023", "item_grp": "0401", "item": "880300-01", "description": "Washer",   "qty": 12, "from_date": "2024-02-01", "to_date": None},

        # -------------------------
        # Version 5
        # -------------------------
        {"sku": "11023", "item_grp": "0005", "item": "version_nr", "description": "5", "qty": None, "from_date": "2024-03-01", "to_date": "2024-03-31"},

        {"sku": "11023", "item_grp": "1200", "item": "990010-01", "description": "Label", "qty": 1, "from_date": "2024-03-01", "to_date": None},

        # -------------------------
        # Version 6
        # -------------------------
        {"sku": "11023", "item_grp": "0006", "item": "version_nr", "description": "6", "qty": None, "from_date": "2024-04-01", "to_date": None},

        {"sku": "11023", "item_grp": "0200", "item": "550412-03", "description": "Steel plate", "qty": 3, "from_date": "2024-04-01", "to_date": None},
    ],

    "11024": [
        # -------------------------
        # Version 7
        # -------------------------
        {"sku": "11024", "item_grp": "0007", "item": "version_nr", "description": "7", "qty": None, "from_date": "2024-01-15", "to_date": "2024-02-14"},

        {"sku": "11024", "item_grp": "0200", "item": "410120-01", "description": "Base frame",     "qty": 1,  "from_date": "2024-01-15", "to_date": None},
        {"sku": "11024", "item_grp": "0300", "item": "420230-01", "description": "Bolt M8",        "qty": 10, "from_date": "2024-01-15", "to_date": "2024-03-14"},
        {"sku": "11024", "item_grp": "0400", "item": "430340-01", "description": "Helper arm",    "qty": 2,  "from_date": "2024-01-15", "to_date": "2024-04-14"},
        {"sku": "11024", "item_grp": "0500", "item": "440450-01", "description": "Lock washer",    "qty": 10, "from_date": "2024-01-15", "to_date": None},
        {"sku": "11024", "item_grp": "0600", "item": "450560-01", "description": "Side panel v1",     "qty": 2,  "from_date": "2024-01-15", "to_date": "2024-02-14"},
        {"sku": "11024", "item_grp": "0700", "item": "460670-01", "description": "Top cover",      "qty": 1,  "from_date": "2024-01-15", "to_date": None},
        {"sku": "11024", "item_grp": "0800", "item": "470780-01", "description": "Rubber foot",    "qty": 4,  "from_date": "2024-01-15", "to_date": "2024-04-14"},
        {"sku": "11024", "item_grp": "0900", "item": "480890-01", "description": "Cable gland",    "qty": 2,  "from_date": "2024-01-15", "to_date": None},
        {"sku": "11024", "item_grp": "1000", "item": "490900-01", "description": "Name plate (eng)",     "qty": 1,  "from_date": "2024-01-15", "to_date": "2027-03-14"},
        {"sku": "11024", "item_grp": "1100", "item": "401010-01", "description": "Inspection tag", "qty": 1,  "from_date": "2024-01-15", "to_date": None},

        # -------------------------
        # Version 8
        # -------------------------
        {"sku": "11024", "item_grp": "0008", "item": "version_nr", "description": "8", "qty": None, "from_date": "2024-02-15", "to_date": "2024-03-14"},

        {"sku": "11024", "item_grp": "0600", "item": "450560-02", "description": "Side panel", "qty": 2, "from_date": "2024-02-15", "to_date": None},
        {"sku": "11024", "item_grp": "1200", "item": "402020-01", "description": "Foam strip", "qty": 2, "from_date": "2024-02-15", "to_date": None},

        # -------------------------
        # Version 9
        # -------------------------
        {"sku": "11024", "item_grp": "0009", "item": "version_nr", "description": "9", "qty": None, "from_date": "2024-03-15", "to_date": "2024-04-14"},

        {"sku": "11024", "item_grp": "0300", "item": "420230-02", "description": "Bolt M8", "qty": 10, "from_date": "2024-03-15", "to_date": None},

        # -------------------------
        # Version 10
        # -------------------------
        {"sku": "11024", "item_grp": "0010", "item": "version_nr", "description": "10", "qty": None, "from_date": "2024-04-15", "to_date": "2027-03-14"},

        {"sku": "11024", "item_grp": "0400", "item": "430340-03", "description": "Support arm",    "qty": 2, "from_date": "2024-04-15", "to_date": None},
        {"sku": "11024", "item_grp": "1300", "item": "403030-01", "description": "Warning sticker","qty": 1, "from_date": "2024-04-15", "to_date": None},
        {"sku": "11024", "item_grp": "0800", "item": "470780-01", "description": "Rubber foot",    "qty": 8, "from_date": "2024-04-15", "to_date": None},

        # -------------------------
        # Version 11
        # -------------------------
        {"sku": "11024", "item_grp": "0011", "item": "version_nr", "description": "11", "qty": None, "from_date": "2027-03-15", "to_date": None},
        {"sku": "11024", "item_grp": "1000", "item": "490900-02", "description": "Name plate", "qty": 1, "from_date": "2027-03-15", "to_date": None},
    ],
}


class ExampleErpBackend:
    def __init__(self, db_path: str | Path = DB_PATH) -> None:
        self.db_path = str(db_path)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def ensure_db_exists(self) -> None:
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS bom_rows (
                    sku TEXT NOT NULL,
                    item_grp TEXT NOT NULL,
                    item TEXT NOT NULL,
                    description TEXT NOT NULL,
                    qty INTEGER,
                    from_date TEXT NOT NULL,
                    to_date TEXT
                )
            """)
            conn.commit()

    def load_example_data(self, fake_db: dict[str, list[dict]]) -> None:
        """
        Helper for demo/dev only.
        Clears the SQLite table and loads FAKE_DB into fakeerp.db.
        Remove later when real ERP data is used.
        """
        self.ensure_db_exists()

        rows_to_insert: list[tuple] = []
        for sku_rows in fake_db.values():
            for row in sku_rows:
                rows_to_insert.append(
                    (
                        row["sku"],
                        row["item_grp"],
                        row["item"],
                        row["description"],
                        row["qty"],
                        row["from_date"],
                        row["to_date"],
                    )
                )

        with self._connect() as conn:
            conn.execute("DELETE FROM bom_rows")
            conn.executemany(
                """
                INSERT INTO bom_rows (
                    sku, item_grp, item, description, qty, from_date, to_date
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                rows_to_insert,
            )
            conn.commit()

    def get_available_skus(self) -> list[str]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT DISTINCT sku FROM bom_rows ORDER BY sku"
            ).fetchall()
        return [row["sku"] for row in rows]

    def _row_is_active_on(self, row: sqlite3.Row, date_str: str) -> bool:
        starts_ok = row["from_date"] <= date_str
        ends_ok = row["to_date"] is None or row["to_date"] >= date_str
        return starts_ok and ends_ok

    def _assert_unique_active_item_groups(self, rows: list[sqlite3.Row]) -> None:
        seen: dict[str, sqlite3.Row] = {}

        for row in rows:
            grp = row["item_grp"]

            current = seen.get(grp)
            if current is None:
                seen[grp] = row
                continue

            raise ValueError(
                f"Multiple active rows with same item_grp '{grp}':\n"
                f"{dict(current)}\n{dict(row)}"
            )

    def _get_rows_for_sku(self, sku: str) -> list[sqlite3.Row]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT sku, item_grp, item, description, qty, from_date, to_date
                FROM bom_rows
                WHERE sku = ?
                ORDER BY from_date, item_grp
                """,
                (sku,),
            ).fetchall()
        return rows

    def _get_effective_rows_on(self, sku: str, date_str: str) -> list[sqlite3.Row]:
        rows = self._get_rows_for_sku(sku)
        active_rows = [row for row in rows if self._row_is_active_on(row, date_str)]

        self._assert_unique_active_item_groups(
            [row for row in active_rows if row["item"] != "version_nr" and row["qty"] is not None]
        )

        return active_rows

    def get_sku_versions(self, sku: str) -> list[dict]:
        rows = self._get_rows_for_sku(sku)
        if not rows:
            return []

        version_rows = [row for row in rows if row["item"] == "version_nr"]
        version_rows.sort(key=lambda r: int(r["description"]))

        versions: list[dict] = []
        today = date.today().isoformat()

        for version_row in version_rows:
            effective_rows = self._get_effective_rows_on(sku, version_row["from_date"])

            bom_rows = [
                {
                    "item_grp": row["item_grp"],
                    "part": row["item"],
                    "desc": row["description"],
                    "qty": row["qty"],
                }
                for row in effective_rows
                if row["item"] != "version_nr" and row["qty"] is not None
            ]

            bom_rows.sort(key=lambda r: r["item_grp"])

            versions.append({
                "version": int(version_row["description"]),
                "from_date": version_row["from_date"],
                "to_date": version_row["to_date"],
                "is_current": (
                    version_row["from_date"] <= today and
                    (version_row["to_date"] is None or version_row["to_date"] >= today)
                ),
                "bom": bom_rows,
            })

        return versions


class Diffing:
    def bom_to_map(self, bom: list[dict]) -> dict[str, dict]:
        result: dict[str, dict] = {}

        for row in bom:
            key = row["item_grp"]

            if key in result:
                raise ValueError(
                    f"Duplicate item_grp in BOM compare map: '{key}'\n"
                    f"{result[key]}\n{row}"
                )

            result[key] = row

        return result

    def rows_equal(self, a: dict, b: dict) -> bool:
        return (
            a["part"] == b["part"] and
            a["qty"] == b["qty"]
        )

    def compare_side_to_center(
        self,
        side_bom: list[dict],
        center_bom: list[dict],
        diff_color: str,
    ) -> list[dict]:
        side_map = self.bom_to_map(side_bom)
        center_map = self.bom_to_map(center_bom)

        result: list[dict] = []

        for key in sorted(side_map):
            side_row = side_map[key]
            center_row = center_map.get(key)

            status = "same"
            if center_row is None or not self.rows_equal(side_row, center_row):
                status = diff_color

            result.append({
                "part": side_row["part"],
                "desc": side_row["desc"],
                "qty": side_row["qty"],
                "status": status,
            })

        return result

    def build_center_rows(
        self,
        left_bom: list[dict] | None,
        center_bom: list[dict],
        right_bom: list[dict] | None,
    ) -> list[dict]:
        left_map = self.bom_to_map(left_bom) if left_bom else {}
        center_map = self.bom_to_map(center_bom)
        right_map = self.bom_to_map(right_bom) if right_bom else {}

        result: list[dict] = []

        for key in sorted(center_map):
            center_row = center_map[key]

            left_row = left_map.get(key)
            right_row = right_map.get(key)

            if left_bom is None:
                differs_from_left = False
            else:
                differs_from_left = left_row is None or not self.rows_equal(left_row, center_row)

            if right_bom is None:
                differs_from_right = False
            else:
                differs_from_right = right_row is None or not self.rows_equal(right_row, center_row)

            result.append({
                "part": center_row["part"],
                "desc": center_row["desc"],
                "qty": center_row["qty"],
                "diff_left": differs_from_left,
                "diff_right": differs_from_right,
            })

        return result


app = Flask(__name__)

erp = ExampleErpBackend("fakeerp.db")
diffing = Diffing()

# Helper for demo/dev only. Delete this later.
erp.load_example_data(FAKE_DB)


def get_triplet(versions: list[dict], center_version_number: int):
    index = next(
        (i for i, v in enumerate(versions) if v["version"] == center_version_number),
        None
    )

    if index is None:
        index = 0

    left_version = versions[index - 1] if index - 1 >= 0 else None
    center_version = versions[index]
    right_version = versions[index + 1] if index + 1 < len(versions) else None

    return left_version, center_version, right_version, index


@app.route("/")
def home():
    skus = erp.get_available_skus()
    if not skus:
        return "No SKUs found"
    return redirect(url_for("show_sku", sku=skus[0]))


@app.route("/sku/<sku>")
def show_sku(sku: str):
    versions = erp.get_sku_versions(sku)
    if not versions:
        return f"SKU not found: {sku}", 404

    center_param = request.args.get("center", type=int)
    if center_param is None:
        center_param = versions[0]["version"]

    left_v, center_v, right_v, index = get_triplet(versions, center_param)

    left_rows = (
        diffing.compare_side_to_center(left_v["bom"], center_v["bom"], diff_color="blue")
        if left_v else []
    )

    center_rows = diffing.build_center_rows(
        left_bom=left_v["bom"] if left_v else None,
        center_bom=center_v["bom"],
        right_bom=right_v["bom"] if right_v else None,
    )

    right_rows = (
        diffing.compare_side_to_center(right_v["bom"], center_v["bom"], diff_color="purple")
        if right_v else []
    )

    prev_center = left_v["version"] if left_v else None
    next_center = right_v["version"] if right_v else None

    return render_template(
        "index.html",
        sku=sku,
        skus=erp.get_available_skus(),
        left_version=left_v,
        center_version=center_v,
        right_version=right_v,
        left_rows=left_rows,
        center_rows=center_rows,
        right_rows=right_rows,
        prev_center=prev_center,
        next_center=next_center,
    )


@app.route("/sku")
def sku_lookup():
    sku = request.args.get("sku", "").strip()
    if not sku:
        skus = erp.get_available_skus()
        if not skus:
            return "No SKUs found"
        return redirect(url_for("show_sku", sku=skus[0]))
    return redirect(url_for("show_sku", sku=sku))


if __name__ == "__main__":
    app.run(debug=True)