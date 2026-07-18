function MemberStats({ expenses, members }) {
  if (members.length === 0) return null

  const stats = members.map((m) => {
    const paid = expenses
      .filter((e) => e.payer === m)
      .reduce((sum, e) => sum + e.amount, 0)
    const shouldPay = expenses
      .filter((e) => e.participants.includes(m))
      .reduce((sum, e) => sum + e.amount / e.participants.length, 0)
    return {
      name: m,
      paid: Math.round(paid * 100) / 100,
      shouldPay: Math.round(shouldPay * 100) / 100,
      balance: Math.round((paid - shouldPay) * 100) / 100,
    }
  })

  return (
    <div className="member-stats">
      <h4>统计概览</h4>
      <table>
        <thead>
          <tr>
            <th>成员</th>
            <th>已付</th>
            <th>应付</th>
            <th>余额</th>
          </tr>
        </thead>
        <tbody>
          {stats.map((s) => (
            <tr key={s.name}>
              <td>{s.name}</td>
              <td>¥{s.paid.toFixed(2)}</td>
              <td>¥{s.shouldPay.toFixed(2)}</td>
              <td className={s.balance >= 0 ? 'positive' : 'negative'}>
                {s.balance >= 0 ? '+' : ''}{s.balance.toFixed(2)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default MemberStats
