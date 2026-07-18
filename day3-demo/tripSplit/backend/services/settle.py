from datetime import datetime


def settle(expenses: list, members: list) -> dict:
    balance = {m: 0.0 for m in members}

    for exp in expenses:
        share = exp["amount"] / len(exp["participants"])
        balance[exp["payer"]] += exp["amount"]
        for p in exp["participants"]:
            balance[p] -= share

    balance = {k: round(v, 2) for k, v in balance.items()}

    debtors = [(name, -amt) for name, amt in balance.items() if amt < -0.001]
    creditors = [(name, amt) for name, amt in balance.items() if amt > 0.001]
    debtors.sort(key=lambda x: x[1], reverse=True)
    creditors.sort(key=lambda x: x[1], reverse=True)

    transfers = []
    i, j = 0, 0
    while i < len(debtors) and j < len(creditors):
        d_name, d_amt = debtors[i]
        c_name, c_amt = creditors[j]
        transfer = min(d_amt, c_amt)
        transfers.append({"from": d_name, "to": c_name, "amount": round(transfer, 2)})
        debtors[i] = (d_name, round(d_amt - transfer, 2))
        creditors[j] = (c_name, round(c_amt - transfer, 2))
        if debtors[i][1] == 0:
            i += 1
        if creditors[j][1] == 0:
            j += 1

    members_stats = []
    for m in members:
        paid = sum(e["amount"] for e in expenses if e["payer"] == m)
        should_pay = sum(
            e["amount"] / len(e["participants"])
            for e in expenses
            if m in e["participants"]
        )
        members_stats.append({
            "name": m,
            "paid": round(paid, 2),
            "shouldPay": round(should_pay, 2),
            "balance": round(paid - should_pay, 2),
        })

    return {
        "totalAmount": round(sum(e["amount"] for e in expenses), 2),
        "members": members_stats,
        "transfers": transfers,
        "settledAt": datetime.now().isoformat(),
    }
