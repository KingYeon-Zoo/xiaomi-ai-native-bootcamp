function EmptyState({ message, actionLabel, onAction }) {
  return (
    <div className="empty-state">
      <p>{message}</p>
      {actionLabel && <button onClick={onAction}>{actionLabel}</button>}
    </div>
  )
}

export default EmptyState
