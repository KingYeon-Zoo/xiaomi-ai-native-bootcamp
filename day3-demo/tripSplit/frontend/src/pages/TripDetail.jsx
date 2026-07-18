import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getTrip, addMember, addExpense, updateExpense, deleteExpense, deleteTrip, settleTrip } from '../api/trips'
import MemberForm from '../components/MemberForm'
import MemberStats from '../components/MemberStats'
import ExpenseForm from '../components/ExpenseForm'
import ExpenseList from '../components/ExpenseList'
import Settlement from '../components/Settlement'
import EmptyState from '../components/EmptyState'

function TripDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [trip, setTrip] = useState(null)
  const [showExpenseForm, setShowExpenseForm] = useState(false)
  const [editingExpense, setEditingExpense] = useState(null)
  const [settlement, setSettlement] = useState(null)

  useEffect(() => {
    loadTrip()
  }, [id])

  async function loadTrip() {
    const data = await getTrip(id)
    setTrip(data)
    setSettlement(data.settlement)
  }

  async function handleAddMember(memberData) {
    await addMember(id, memberData)
    loadTrip()
  }

  async function handleAddExpense(expenseData) {
    await addExpense(id, expenseData)
    setShowExpenseForm(false)
    loadTrip()
  }

  async function handleUpdateExpense(expenseData) {
    await updateExpense(id, editingExpense.id, expenseData)
    setEditingExpense(null)
    loadTrip()
  }

  async function handleDeleteExpense(expenseId) {
    await deleteExpense(id, expenseId)
    loadTrip()
  }

  async function handleSettle() {
    const result = await settleTrip(id)
    setSettlement(result)
    loadTrip()
  }

  async function handleDeleteTrip() {
    await deleteTrip(id)
    navigate('/')
  }

  if (!trip) return <div>加载中...</div>

  return (
    <div className="trip-detail-page">
      <header>
        <button onClick={() => navigate('/')}>← 返回</button>
        <h1>{trip.name}</h1>
        <span>{trip.startDate} ~ {trip.endDate}</span>
        <button className="danger" onClick={handleDeleteTrip}>删除旅行</button>
      </header>

      <div className="detail-content">
        <aside className="members-section">
          <h3>👤 成员</h3>
          <ul className="member-list">
            {trip.members.map((m) => (
              <li key={m}>{m}</li>
            ))}
          </ul>
          {trip.members.length < 20 && (
            <MemberForm existingMembers={trip.members} onSubmit={handleAddMember} />
          )}
          <MemberStats expenses={trip.expenses} members={trip.members} />
        </aside>

        <main className="expenses-section">
          <div className="expenses-header">
            <h3>📋 账单</h3>
            <button onClick={() => { setShowExpenseForm(true); setEditingExpense(null); }}>+ 添加</button>
          </div>

          {(showExpenseForm || editingExpense) && (
            <ExpenseForm
              members={trip.members}
              initialData={editingExpense}
              onSubmit={editingExpense ? handleUpdateExpense : handleAddExpense}
              onCancel={() => { setShowExpenseForm(false); setEditingExpense(null); }}
            />
          )}

          {trip.expenses.length === 0 ? (
            <EmptyState message="暂无账单，添加第一笔吧！" />
          ) : (
            <ExpenseList
              expenses={trip.expenses}
              onEdit={(exp) => { setEditingExpense(exp); setShowExpenseForm(false); }}
              onDelete={handleDeleteExpense}
            />
          )}
        </main>
      </div>

      <section className="settlement-section">
        <button className="primary" onClick={handleSettle} disabled={trip.expenses.length === 0}>
          💰 生成结算
        </button>
        <Settlement settlement={settlement} />
      </section>
    </div>
  )
}

export default TripDetail
