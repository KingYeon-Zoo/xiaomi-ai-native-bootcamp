from services.settle import settle


def test_settle_three_people():
    expenses = [
        {"name": "酒店", "amount": 900, "payer": "小王", "participants": ["小王", "小李", "小张"]},
        {"name": "晚饭", "amount": 360, "payer": "小李", "participants": ["小王", "小李", "小张"]},
        {"name": "打车", "amount": 80, "payer": "小张", "participants": ["小王", "小张"]},
    ]
    result = settle(expenses, ["小王", "小李", "小张"])
    members = {m["name"]: m for m in result["members"]}
    assert members["小王"]["balance"] == 440
    assert members["小李"]["balance"] == -60
    assert members["小张"]["balance"] == -380
    transfers = {(t["from"], t["to"]): t["amount"] for t in result["transfers"]}
    assert transfers[("小张", "小王")] == 380
    assert transfers[("小李", "小王")] == 60


def test_settle_two_people():
    expenses = [
        {"name": "午饭", "amount": 100, "payer": "A", "participants": ["A", "B"]},
    ]
    result = settle(expenses, ["A", "B"])
    members = {m["name"]: m for m in result["members"]}
    assert members["A"]["balance"] == 50
    assert members["B"]["balance"] == -50
    assert len(result["transfers"]) == 1
    assert result["transfers"][0]["from"] == "B"
    assert result["transfers"][0]["to"] == "A"
    assert result["transfers"][0]["amount"] == 50


def test_settle_float_precision():
    expenses = [
        {"name": "测试", "amount": 100.01, "payer": "A", "participants": ["A", "B", "C"]},
    ]
    result = settle(expenses, ["A", "B", "C"])
    for m in result["members"]:
        assert round(m["balance"], 2) == round(m["balance"], 2)
    total_transfer = sum(t["amount"] for t in result["transfers"])
    assert round(total_transfer, 2) == round(100.01 / 3 * 2, 2)


def test_settle_total_amount_match():
    expenses = [
        {"name": "酒店", "amount": 900, "payer": "小王", "participants": ["小王", "小李", "小张"]},
        {"name": "晚饭", "amount": 360, "payer": "小李", "participants": ["小王", "小李", "小张"]},
        {"name": "打车", "amount": 80, "payer": "小张", "participants": ["小王", "小张"]},
    ]
    result = settle(expenses, ["小王", "小李", "小张"])
    total_expense = sum(e["amount"] for e in expenses)
    total_transfer = sum(t["amount"] for t in result["transfers"])
    assert round(total_transfer, 2) == round(sum(
        m["balance"] for m in result["members"] if m["balance"] > 0
    ), 2)


def test_settle_balance_sum_zero():
    expenses = [
        {"name": "酒店", "amount": 900, "payer": "小王", "participants": ["小王", "小李", "小张"]},
        {"name": "晚饭", "amount": 360, "payer": "小李", "participants": ["小王", "小李", "小张"]},
        {"name": "打车", "amount": 80, "payer": "小张", "participants": ["小王", "小张"]},
    ]
    result = settle(expenses, ["小王", "小李", "小张"])
    total_balance = sum(m["balance"] for m in result["members"])
    assert round(total_balance, 2) == 0
