import csv
import json

from utils.formatter import build_result_rows, export_csv, export_json


class TestBuildResultRows:
    def test_sorts_by_port(self) -> None:
        rows = build_result_rows([(80, "banner"), (22, "")])
        assert [r["port"] for r in rows] == [22, 80]

    def test_marks_state_open(self) -> None:
        rows = build_result_rows([(22, "SSH-2.0")])
        assert rows[0]["state"] == "open"

    def test_empty_banner_becomes_placeholder(self) -> None:
        rows = build_result_rows([(80, "")])
        assert rows[0]["service"] == "(no banner)"

    def test_preserves_banner_text(self) -> None:
        rows = build_result_rows([(22, "SSH-2.0-OpenSSH")])
        assert rows[0]["service"] == "SSH-2.0-OpenSSH"


class TestExportJson:
    def test_writes_valid_json(self, tmp_path) -> None:
        rows = build_result_rows([(22, "SSH")])
        path = tmp_path / "out.json"
        export_json(rows, str(path))
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data == rows


class TestExportCsv:
    def test_writes_valid_csv(self, tmp_path) -> None:
        rows = build_result_rows([(22, "SSH")])
        path = tmp_path / "out.csv"
        export_csv(rows, str(path))
        with open(path, newline="", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
        assert reader[0]["port"] == "22"
        assert reader[0]["service"] == "SSH"
