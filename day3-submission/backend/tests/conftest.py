import json
import tempfile
import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from unittest.mock import patch


@pytest.fixture
def client(tmp_path):
    data_file = tmp_path / "trips.json"
    data_file.write_text('{"trips": []}', encoding="utf-8")
    with patch("services.storage.DATA_FILE", data_file):
        from main import app
        with TestClient(app) as c:
            yield c


@pytest.fixture
def sample_trip(client):
    r = client.post("/trips", json={
        "name": "南京游",
        "startDate": "2026-07-01",
        "endDate": "2026-07-03",
    })
    return r.json()


@pytest.fixture
def trip_with_members(client, sample_trip):
    tid = sample_trip["id"]
    for name in ["小王", "小李", "小张"]:
        client.post(f"/trips/{tid}/members", json={"name": name})
    return sample_trip
