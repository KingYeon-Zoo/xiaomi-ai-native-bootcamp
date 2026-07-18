function Settlement({ settlement }) {
  if (!settlement) return null

  return (
    <div className="settlement">
      <h3>结算结果</h3>
      <p className="total-amount">总支出：¥{settlement.totalAmount.toFixed(2)}</p>
      <table className="settlement-table">
        <thead>
          <tr>
            <th>成员</th>
            <th>已付</th>
            <th>应付</th>
            <th>余额</th>
          </tr>
        </thead>
        <tbody>
          {settlement.members.map((m) => (
            <tr key={m.name}>
              <td>{m.name}</td>
              <td>¥{m.paid.toFixed(2)}</td>
              <td>¥{m.shouldPay.toFixed(2)}</td>
              <td className={m.balance >= 0 ? 'positive' : 'negative'}>
                {m.balance >= 0 ? '+' : ''}{m.balance.toFixed(2)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <h4>转账方案</h4>
      <div className="transfers">
        {settlement.transfers.map((t, i) => (
          <div key={i} className="transfer-item">
            {t.from} → {t.to}：<strong>¥{t.amount.toFixed(2)}</strong>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Settlement
