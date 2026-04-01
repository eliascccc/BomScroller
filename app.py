from __future__ import annotations

from flask import Flask, render_template, request, redirect, url_for

FAKE_DB = {
    "11023": [
        # -------------------------
        # Version 3
        # -------------------------
        {
            "sku": "11023",
            "item_nr": "0003",
            "item": "version_nr",
            "description": "3",
            "qty": None,
            "from_date": "2024-01-01",
            "to_date": "2024-01-31",
        },
        {
            "sku": "11023",
            "item_nr": "0200",
            "item": "550412-02",
            "description": "Steel plate",
            "qty": 2,
            "from_date": "2024-01-01",
            "to_date": "2024-03-31",
        },
        {
            "sku": "11023",
            "item_nr": "0300",
            "item": "660221-01",
            "description": "Screw M6",
            "qty": 8,
            "from_date": "2024-01-01",
            "to_date": "2024-01-31",
        },
        {
            "sku": "11023",
            "item_nr": "0400",
            "item": "770100-01",
            "description": "Bracket",
            "qty": 1,
            "from_date": "2024-01-01",
            "to_date": "2024-02-29",
        },

        # -------------------------
        # Version 4
        # -------------------------
        {
            "sku": "11023",
            "item_nr": "0004",
            "item": "version_nr",
            "description": "4",
            "qty": None,
            "from_date": "2024-02-01",
            "to_date": "2024-02-29",
        },

        # qty change -> new revision of same screw
        {
            "sku": "11023",
            "item_nr": "0301",
            "item": "660221-02",
            "description": "Screw M6",
            "qty": 12,
            "from_date": "2024-02-01",
            "to_date": None,
        },

        # new washer
        {
            "sku": "11023",
            "item_nr": "0401",
            "item": "880300-01",
            "description": "Washer",
            "qty": 12,
            "from_date": "2024-02-01",
            "to_date": None,
        },

        # -------------------------
        # Version 5
        # -------------------------
        {
            "sku": "11023",
            "item_nr": "0005",
            "item": "version_nr",
            "description": "5",
            "qty": None,
            "from_date": "2024-03-01",
            "to_date": "2024-03-31",
        },

        # new label
        {
            "sku": "11023",
            "item_nr": "0500",
            "item": "990010-01",
            "description": "Label",
            "qty": 1,
            "from_date": "2024-03-01",
            "to_date": None,
        },

        # -------------------------
        # Version 6
        # -------------------------
        {
            "sku": "11023",
            "item_nr": "0006",
            "item": "version_nr",
            "description": "6",
            "qty": None,
            "from_date": "2024-04-01",
            "to_date": None,
        },

        # steel plate revision change
        {
            "sku": "11023",
            "item_nr": "0201",
            "item": "550412-03",
            "description": "Steel plate",
            "qty": 3,
            "from_date": "2024-04-01",
            "to_date": None,
        },
    ]
}
class Data:
    def __init__(self) -> None:
        self.FAKE_DB = FAKE_DB

    def get_available_skus(self) -> list[str]:
        return sorted(self.FAKE_DB.keys())

    def _row_is_active_on(self, row: dict, date_str: str) -> bool:
        starts_ok = row["from_date"] <= date_str
        ends_ok = row["to_date"] is None or row["to_date"] >= date_str
        return starts_ok and ends_ok

    def _base_item(self, item: str) -> str:
        if item == "version_nr":
            return item
        return item.split("-")[0]

    def _pick_latest_row_per_base_item(self, rows: list[dict]) -> list[dict]:
        """
        If multiple active rows exist for the same base article (e.g. 550412-02 and 550412-03),
        keep only the latest one.
        """
        chosen: dict[str, dict] = {}

        for row in rows:
            base = self._base_item(row["item"])

            current = chosen.get(base)
            if current is None:
                chosen[base] = row
                continue

            # Choose latest by from_date, then item_nr as tie-breaker
            current_key = (current["from_date"], current["item_nr"])
            new_key = (row["from_date"], row["item_nr"])

            if new_key > current_key:
                chosen[base] = row

        return list(chosen.values())

    def _get_effective_rows_on(self, sku: str, date_str: str) -> list[dict]:
        rows = self.FAKE_DB.get(sku, [])
        active_rows = [row for row in rows if self._row_is_active_on(row, date_str)]
        return self._pick_latest_row_per_base_item(active_rows)

    def get_sku_versions(self, sku: str) -> list[dict]:
        rows = self.FAKE_DB.get(sku, [])
        if not rows:
            return []

        version_rows = [row for row in rows if row["item"] == "version_nr"]
        version_rows.sort(key=lambda r: int(r["description"]))

        versions: list[dict] = []

        for version_row in version_rows:
            effective_rows = self._get_effective_rows_on(sku, version_row["from_date"])

            bom_rows = [
                {
                    "item_nr": row["item_nr"],
                    "part": row["item"],
                    "base_part": self._base_item(row["item"]),
                    "desc": row["description"],
                    "qty": row["qty"],
                }
                for row in effective_rows
                if row["item"] != "version_nr"
            ]

            bom_rows.sort(key=lambda r: r["item_nr"])

            versions.append({
                "version": int(version_row["description"]),
                "date": version_row["from_date"],
                "bom": bom_rows,
            })

        return versions
    

class Diffing:
    def bom_to_map(self, bom: list[dict]) -> dict[str, dict]:
        return {row["base_part"]: row for row in bom}

    def rows_equal(self, a: dict, b: dict) -> bool:
        return (
            a["part"] == b["part"] and
            a["desc"] == b["desc"] and
            a["qty"] == b["qty"]
        )

    def compare_side_to_center(
        self,
        side_bom: list[dict],
        center_bom: list[dict],
        diff_color: str,   # "blue" or "purple"
    ) -> list[dict]:
        side_map = self.bom_to_map(side_bom)
        center_map = self.bom_to_map(center_bom)

        all_keys = sorted(set(side_map) | set(center_map))
        result: list[dict] = []

        for key in all_keys:
            side_row = side_map.get(key)
            center_row = center_map.get(key)

            if side_row is None and center_row is not None:
                result.append({
                    "part": center_row["part"],
                    "desc": center_row["desc"],
                    "qty": "",
                    "status": diff_color,
                })
            elif side_row is not None and center_row is None:
                result.append({
                    "part": side_row["part"],
                    "desc": side_row["desc"],
                    "qty": side_row["qty"],
                    "status": diff_color,
                })
            else:
                assert side_row is not None
                assert center_row is not None

                status = "same" if self.rows_equal(side_row, center_row) else diff_color

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

            differs_from_left = left_row is None or not self.rows_equal(left_row, center_row)
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

data = Data()
diffing = Diffing()


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
    skus = data.get_available_skus()
    if not skus:
        return "No SKUs found"
    return redirect(url_for("show_sku", sku=skus[0]))


@app.route("/sku/<sku>")
def show_sku(sku: str):
    versions = data.get_sku_versions(sku)
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
        skus=data.get_available_skus(),
        left_version=left_v,
        center_version=center_v,
        right_version=right_v,
        left_rows=left_rows,
        center_rows=center_rows,
        right_rows=right_rows,
        prev_center=prev_center,
        next_center=next_center,
    )


if __name__ == "__main__":
    app.run(debug=True)