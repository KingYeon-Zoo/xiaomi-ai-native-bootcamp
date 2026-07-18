import uuid
from fastapi import APIRouter, HTTPException
from models import TripCreate, MemberAdd, ExpenseCreate, ExpenseUpdate
from services.storage import read_trips, write_trips

router = APIRouter()


@router.post("/trips")
def create_trip(trip: TripCreate):
    if not trip.name.strip():
        raise HTTPException(400, "旅行名称不能为空")
    if trip.startDate > trip.endDate:
        raise HTTPException(400, "开始日期不能晚于结束日期")
    data = read_trips()
    new_trip = {
        "id": str(uuid.uuid4()),
        "name": trip.name,
        "startDate": trip.startDate,
        "endDate": trip.endDate,
        "members": [],
        "expenses": [],
        "settlement": None,
    }
    data["trips"].append(new_trip)
    write_trips(data)
    return new_trip


@router.get("/trips")
def get_trips():
    data = read_trips()
    result = []
    for t in data["trips"]:
        result.append({
            "id": t["id"],
            "name": t["name"],
            "startDate": t["startDate"],
            "endDate": t["endDate"],
            "memberCount": len(t["members"]),
            "expenseCount": len(t["expenses"]),
        })
    return {"trips": result}


@router.get("/trips/{trip_id}")
def get_trip(trip_id: str):
    data = read_trips()
    for t in data["trips"]:
        if t["id"] == trip_id:
            return t
    raise HTTPException(404, "旅行不存在")


@router.delete("/trips/{trip_id}", status_code=204)
def delete_trip(trip_id: str):
    data = read_trips()
    for i, t in enumerate(data["trips"]):
        if t["id"] == trip_id:
            data["trips"].pop(i)
            write_trips(data)
            return
    raise HTTPException(404, "旅行不存在")


@router.post("/trips/{trip_id}/members")
def add_member(trip_id: str, member: MemberAdd):
    if not member.name.strip():
        raise HTTPException(400, "成员名不能为空")
    data = read_trips()
    trip = _get_trip(data, trip_id)
    if member.name in trip["members"]:
        raise HTTPException(400, "成员名已存在")
    trip["members"].append(member.name)
    write_trips(data)
    return {"members": trip["members"]}


@router.post("/trips/{trip_id}/expenses")
def add_expense(trip_id: str, expense: ExpenseCreate):
    if expense.amount <= 0:
        raise HTTPException(400, "金额必须大于 0")
    if not expense.participants:
        raise HTTPException(400, "至少选择一个参与人")
    data = read_trips()
    trip = _get_trip(data, trip_id)
    if expense.payer not in trip["members"]:
        raise HTTPException(400, "付款人不在成员列表中")
    for p in expense.participants:
        if p not in trip["members"]:
            raise HTTPException(400, f"参与人 {p} 不在成员列表中")
    new_expense = {
        "id": str(uuid.uuid4()),
        "name": expense.name,
        "amount": expense.amount,
        "payer": expense.payer,
        "participants": expense.participants,
        "category": expense.category,
        "date": expense.date,
        "note": expense.note or "",
    }
    trip["expenses"].append(new_expense)
    trip["settlement"] = None
    write_trips(data)
    return new_expense


@router.put("/trips/{trip_id}/expenses/{expense_id}")
def update_expense(trip_id: str, expense_id: str, expense: ExpenseUpdate):
    data = read_trips()
    trip = _get_trip(data, trip_id)
    exp = _get_expense(trip, expense_id)

    update_data = expense.model_dump(exclude_none=True)
    if "amount" in update_data and update_data["amount"] <= 0:
        raise HTTPException(400, "金额必须大于 0")
    if "participants" in update_data and not update_data["participants"]:
        raise HTTPException(400, "至少选择一个参与人")
    if "payer" in update_data and update_data["payer"] not in trip["members"]:
        raise HTTPException(400, "付款人不在成员列表中")
    if "participants" in update_data:
        for p in update_data["participants"]:
            if p not in trip["members"]:
                raise HTTPException(400, f"参与人 {p} 不在成员列表中")

    for key, value in update_data.items():
        exp[key] = value
    trip["settlement"] = None
    write_trips(data)
    return exp


@router.delete("/trips/{trip_id}/expenses/{expense_id}", status_code=204)
def delete_expense(trip_id: str, expense_id: str):
    data = read_trips()
    trip = _get_trip(data, trip_id)
    for i, e in enumerate(trip["expenses"]):
        if e["id"] == expense_id:
            trip["expenses"].pop(i)
            trip["settlement"] = None
            write_trips(data)
            return
    raise HTTPException(404, "账单不存在")


@router.post("/trips/{trip_id}/settle")
def settle_trip(trip_id: str):
    from services.settle import settle
    data = read_trips()
    trip = _get_trip(data, trip_id)
    if not trip["expenses"]:
        raise HTTPException(400, "请先添加账单")
    result = settle(trip["expenses"], trip["members"])
    trip["settlement"] = result
    write_trips(data)
    return result


def _get_trip(data: dict, trip_id: str) -> dict:
    for t in data["trips"]:
        if t["id"] == trip_id:
            return t
    raise HTTPException(404, "旅行不存在")


def _get_expense(trip: dict, expense_id: str) -> dict:
    for e in trip["expenses"]:
        if e["id"] == expense_id:
            return e
    raise HTTPException(404, "账单不存在")
