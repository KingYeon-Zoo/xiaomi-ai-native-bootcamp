import { useState } from 'react'

function TripForm({ onSubmit }) {
  const [name, setName] = useState('')
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')
  const [error, setError] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!name.trim()) {
      setError('旅行名称不能为空')
      return
    }
    setError('')
    onSubmit({ name: name.trim(), startDate, endDate })
  }

  return (
    <form className="trip-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <label>旅行名称</label>
        <input value={name} onChange={(e) => setName(e.target.value)} placeholder="例如：南京 3 日游" />
      </div>
      <div className="form-group">
        <label>开始日期</label>
        <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
      </div>
      <div className="form-group">
        <label>结束日期</label>
        <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
      </div>
      {error && <p className="error">{error}</p>}
      <button type="submit">创建旅行</button>
    </form>
  )
}

export default TripForm
