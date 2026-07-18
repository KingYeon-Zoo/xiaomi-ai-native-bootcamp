import { useState, useEffect } from 'react'

const CATEGORIES = ['住宿', '餐饮', '交通', '门票', '购物', '其他']

function ExpenseForm({ members, initialData, onSubmit, onCancel }) {
  const isEdit = !!initialData
  const today = new Date().toISOString().split('T')[0]

  const [name, setName] = useState(initialData?.name || '')
  const [amount, setAmount] = useState(initialData?.amount?.toString() || '')
  const [payer, setPayer] = useState(initialData?.payer || '')
  const [participants, setParticipants] = useState(initialData?.participants || [])
  const [category, setCategory] = useState(initialData?.category || '住宿')
  const [customCategory, setCustomCategory] = useState('')
  const [date, setDate] = useState(initialData?.date || today)
  const [note, setNote] = useState(initialData?.note || '')
  const [error, setError] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    const amountNum = parseFloat(amount)
    if (isNaN(amountNum) || amountNum <= 0) {
      setError('金额必须大于 0')
      return
    }
    if (participants.length === 0) {
      setError('至少选择一个参与人')
      return
    }
    setError('')
    onSubmit({
      name: name.trim(),
      amount: amountNum,
      payer,
      participants,
      category: category === '其他' && customCategory.trim() ? customCategory.trim() : category,
      date,
      note: note.trim(),
    })
  }

  const toggleParticipant = (member) => {
    setParticipants((prev) =>
      prev.includes(member) ? prev.filter((m) => m !== member) : [...prev, member]
    )
  }

  return (
    <form className="expense-form" onSubmit={handleSubmit}>
      <h3>{isEdit ? '编辑账单' : '添加账单'}</h3>
      <div className="form-group">
        <label>名称</label>
        <input value={name} onChange={(e) => setName(e.target.value)} placeholder="例如：酒店" />
      </div>
      <div className="form-group">
        <label>金额 (¥)</label>
        <input type="number" step="0.01" value={amount} onChange={(e) => setAmount(e.target.value)} placeholder="0.00" />
      </div>
      <div className="form-group">
        <label>付款人</label>
        <select value={payer} onChange={(e) => setPayer(e.target.value)}>
          <option value="">请选择</option>
          {members.map((m) => (
            <option key={m} value={m}>{m}</option>
          ))}
        </select>
      </div>
      <div className="form-group">
        <label>参与人</label>
        <div className="checkbox-group">
          {members.map((m) => (
            <label key={m} className="checkbox-label">
              <input type="checkbox" checked={participants.includes(m)} onChange={() => toggleParticipant(m)} />
              {m}
            </label>
          ))}
        </div>
      </div>
      <div className="form-group">
        <label>分类</label>
        <select value={category} onChange={(e) => setCategory(e.target.value)}>
          {CATEGORIES.map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>
        {category === '其他' && (
          <input value={customCategory} onChange={(e) => setCustomCategory(e.target.value)} placeholder="自定义分类" />
        )}
      </div>
      <div className="form-group">
        <label>日期</label>
        <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
      </div>
      <div className="form-group">
        <label>备注</label>
        <input value={note} onChange={(e) => setNote(e.target.value)} placeholder="选填" />
      </div>
      {error && <p className="error">{error}</p>}
      <div className="form-actions">
        <button type="submit">{isEdit ? '保存' : '添加'}</button>
        {onCancel && <button type="button" onClick={onCancel}>取消</button>}
      </div>
    </form>
  )
}

export default ExpenseForm
