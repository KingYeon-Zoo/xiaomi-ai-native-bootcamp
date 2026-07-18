const BASE = '/trips'

export async function getTrips() {
  const res = await fetch(BASE)
  return res.json()
}

export async function getTrip(id) {
  const res = await fetch(`${BASE}/${id}`)
  return res.json()
}

export async function createTrip(data) {
  const res = await fetch(BASE, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  return res.json()
}

export async function deleteTrip(id) {
  await fetch(`${BASE}/${id}`, { method: 'DELETE' })
}

export async function addMember(tripId, data) {
  const res = await fetch(`${BASE}/${tripId}/members`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  return res.json()
}

export async function addExpense(tripId, data) {
  const res = await fetch(`${BASE}/${tripId}/expenses`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  return res.json()
}

export async function updateExpense(tripId, expenseId, data) {
  const res = await fetch(`${BASE}/${tripId}/expenses/${expenseId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  return res.json()
}

export async function deleteExpense(tripId, expenseId) {
  await fetch(`${BASE}/${tripId}/expenses/${expenseId}`, { method: 'DELETE' })
}

export async function settleTrip(tripId) {
  const res = await fetch(`${BASE}/${tripId}/settle`, { method: 'POST' })
  return res.json()
}
