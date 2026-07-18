def _expense_data(**overrides):
    data = {
        "name": "酒店",
        "amount": 900,
        "payer": "小王",
        "participants": ["小王", "小李"],
        "category": "住宿",
        "date": "2026-07-01",
    }
    data.update(overrides)
    return data


def test_add_expense(client, trip_with_members):
    tid = trip_with_members["id"]
    r = client.post(f"/trips/{tid}/expenses", json=_expense_data())
    assert r.status_code == 200
    assert r.json()["name"] == "酒店"


def test_add_expense_zero_amount(client, trip_with_members):
    tid = trip_with_members["id"]
    r = client.post(f"/trips/{tid}/expenses", json=_expense_data(amount=0))
    assert r.status_code == 400


def test_add_expense_negative_amount(client, trip_with_members):
    tid = trip_with_members["id"]
    r = client.post(f"/trips/{tid}/expenses", json=_expense_data(amount=-100))
    assert r.status_code == 400


def test_add_expense_payer_not_member(client, trip_with_members):
    tid = trip_with_members["id"]
    r = client.post(f"/trips/{tid}/expenses", json=_expense_data(payer="不存在的人"))
    assert r.status_code == 400


def test_add_expense_empty_participants(client, trip_with_members):
    tid = trip_with_members["id"]
    r = client.post(f"/trips/{tid}/expenses", json=_expense_data(participants=[]))
    assert r.status_code == 400


def test_update_expense_partial(client, trip_with_members):
    tid = trip_with_members["id"]
    r = client.post(f"/trips/{tid}/expenses", json=_expense_data())
    eid = r.json()["id"]
    r2 = client.put(f"/trips/{tid}/expenses/{eid}", json={"amount": 800})
    assert r2.status_code == 200
    assert r2.json()["amount"] == 800
    assert r2.json()["name"] == "酒店"


def test_delete_expense(client, trip_with_members):
    tid = trip_with_members["id"]
    r = client.post(f"/trips/{tid}/expenses", json=_expense_data())
    eid = r.json()["id"]
    r2 = client.delete(f"/trips/{tid}/expenses/{eid}")
    assert r2.status_code == 204


def test_settlement_cleared_on_edit(client, trip_with_members):
    tid = trip_with_members["id"]
    client.post(f"/trips/{tid}/expenses", json=_expense_data())
    client.post(f"/trips/{tid}/settle")
    r = client.get(f"/trips/{tid}")
    assert r.json()["settlement"] is not None

    eid = r.json()["expenses"][0]["id"]
    client.put(f"/trips/{tid}/expenses/{eid}", json={"amount": 800})
    r2 = client.get(f"/trips/{tid}")
    assert r2.json()["settlement"] is None


def test_settlement_cleared_on_delete(client, trip_with_members):
    tid = trip_with_members["id"]
    r = client.post(f"/trips/{tid}/expenses", json=_expense_data())
    client.post(f"/trips/{tid}/settle")
    r2 = client.get(f"/trips/{tid}")
    assert r2.json()["settlement"] is not None

    eid = r.json()["id"]
    client.delete(f"/trips/{tid}/expenses/{eid}")
    r3 = client.get(f"/trips/{tid}")
    assert r3.json()["settlement"] is None
