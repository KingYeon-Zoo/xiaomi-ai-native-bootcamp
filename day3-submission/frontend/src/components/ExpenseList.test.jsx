import { render, screen, fireEvent } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import ExpenseList from './ExpenseList'

const expenses = [
  { id: '1', name: '酒店', amount: 900, payer: '小王', category: '住宿', date: '2026-07-01', participants: ['小王', '小李'] },
  { id: '2', name: '晚饭', amount: 360, payer: '小李', category: '餐饮', date: '2026-07-01', participants: ['小王', '小李'] },
  { id: '3', name: '打车', amount: 80, payer: '小张', category: '交通', date: '2026-07-02', participants: ['小王', '小张'] },
]

describe('ExpenseList', () => {
  it('列表渲染', () => {
    render(<ExpenseList expenses={expenses} onEdit={() => {}} onDelete={() => {}} />)

    expect(screen.getByText('酒店')).toBeInTheDocument()
    expect(screen.getByText('晚饭')).toBeInTheDocument()
    expect(screen.getByText('打车')).toBeInTheDocument()
    expect(screen.getByText('¥900.00')).toBeInTheDocument()
    expect(screen.getByText('小王付')).toBeInTheDocument()
    expect(screen.getByText('住宿')).toBeInTheDocument()
  })

  it('编辑回调', () => {
    const onEdit = vi.fn()
    render(<ExpenseList expenses={expenses} onEdit={onEdit} onDelete={() => {}} />)

    const editButtons = screen.getAllByText('编辑')
    fireEvent.click(editButtons[0])

    expect(onEdit).toHaveBeenCalled()
  })

  it('删除回调', () => {
    const onDelete = vi.fn()
    render(<ExpenseList expenses={expenses} onEdit={() => {}} onDelete={onDelete} />)

    const deleteButtons = screen.getAllByText('删除')
    fireEvent.click(deleteButtons[0])

    expect(onDelete).toHaveBeenCalledWith('3')
  })
})
