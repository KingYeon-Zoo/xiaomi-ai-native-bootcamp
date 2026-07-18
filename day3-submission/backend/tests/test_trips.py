def test_create_trip(client):
    r = client.post("/trips", json={
        "name": "南京游",
        "startDate": "2026-07-01",
        "endDate": "2026-07-03",
    })
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == "南京游"
    assert "id" in data


def test_create_trip_empty_name(client):
    r = client.post("/trips", json={
        "name": "",
        "startDate": "2026-07-01",
        "endDate": "2026-07-03",
    })
    assert r.status_code == 400


def test_create_trip_dates_reversed(client):
    r = client.post("/trips", json={
        "name": "测试",
        "startDate": "2026-07-03",
        "endDate": "2026-07-01",
    })
    assert r.status_code == 400


def test_get_trips(client, sample_trip):
    r = client.get("/trips")
    assert r.status_code == 200
    trips = r.json()["trips"]
    assert len(trips) >= 1
    assert "memberCount" in trips[0]
    assert "expenseCount" in trips[0]


def test_get_trip_detail(client, sample_trip):
    tid = sample_trip["id"]
    r = client.get(f"/trips/{tid}")
    assert r.status_code == 200
    assert r.json()["id"] == tid


def test_get_trip_not_found(client):
    r = client.get("/trips/nonexistent")
    assert r.status_code == 404


def test_delete_trip(client, sample_trip):
    tid = sample_trip["id"]
    r = client.delete(f"/trips/{tid}")
    assert r.status_code == 204
    r2 = client.get(f"/trips/{tid}")
    assert r2.status_code == 404


def test_delete_trip_not_found(client):
    r = client.delete("/trips/nonexistent")
    assert r.status_code == 404
