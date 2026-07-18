def test_add_member(client, sample_trip):
    tid = sample_trip["id"]
    r = client.post(f"/trips/{tid}/members", json={"name": "小王"})
    assert r.status_code == 200
    assert "小王" in r.json()["members"]


def test_add_member_empty_name(client, sample_trip):
    tid = sample_trip["id"]
    r = client.post(f"/trips/{tid}/members", json={"name": ""})
    assert r.status_code == 400


def test_add_member_duplicate(client, sample_trip):
    tid = sample_trip["id"]
    client.post(f"/trips/{tid}/members", json={"name": "小王"})
    r = client.post(f"/trips/{tid}/members", json={"name": "小王"})
    assert r.status_code == 400
