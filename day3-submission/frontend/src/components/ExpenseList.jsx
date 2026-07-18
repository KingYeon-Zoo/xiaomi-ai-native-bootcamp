function ExpenseList({ expenses, onEdit, onDelete }) {
  if (expenses.length === 0) {
    return <p className="empty-hint">暂无账单</p>
  }

  const sorted = [...expenses].sort((a, b) => b.date.localeCompare(a.date))

  return (
    <div className="expense-list">
      {sorted.map((exp) => (
        <div key={exp.id} className="expense-item">
          <div className="expense-info">
            <span className="expense-name">{exp.name}</span>
            <span className="expense-amount">¥{exp.amount.toFixed(2)}</span>
            <span className="expense-payer">{exp.payer}付</span>
            <span className="expense-category">{exp.category}</span>
            <span className="expense-date">{exp.date}</span>
          </div>
          <div className="expense-actions">
            <button onClick={() => onEdit(exp)}>编辑</button>
            <button onClick={() => onDelete(exp.id)}>删除</button>
          </div>
        </div>
      ))}
    </div>
  )
}

export default ExpenseList
