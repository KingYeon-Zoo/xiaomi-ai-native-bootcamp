import { useState } from 'react'

function MemberForm({ existingMembers, onSubmit }) {
  const [name, setName] = useState('')
  const [error, setError] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!name.trim()) {
      setError('成员名不能为空')
      return
    }
    if (existingMembers.includes(name.trim())) {
      setError('成员名已存在')
      return
    }
    setError('')
    onSubmit({ name: name.trim() })
    setName('')
  }

  return (
    <form className="member-form" onSubmit={handleSubmit}>
      <input value={name} onChange={(e) => setName(e.target.value)} placeholder="输入成员名" />
      <button type="submit">添加</button>
      {error && <p className="error">{error}</p>}
    </form>
  )
}

export default MemberForm
