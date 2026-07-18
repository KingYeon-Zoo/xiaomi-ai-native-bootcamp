import { render, screen, fireEvent } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import ExpenseForm from './ExpenseForm'

const members = ['小王', '小李', '小张']

describe('ExpenseForm', () => {
  it('添加成功', () => {
    const onSubmit = vi.fn()
    render(<ExpenseForm members={members} onSubmit={onSubmit} />)

    fireEvent.change(screen.getByPlaceholderText('例如：酒店'), {
      target: { value: '酒店' },
    })
    fireEvent.change(screen.getByPlaceholderText('0.00'), {
      target: { value: '900' },
    })
    fireEvent.change(screen.getByDisplayValue('请选择'), {
      target: { value: '小王' },
    })
    fireEvent.click(screen.getByLabelText('小王'))
    fireEvent.click(screen.getByLabelText('小李'))

    fireEvent.click(screen.getByText('添加'))

    expect(onSubmit).toHaveBeenCalled()
  })

  it('金额为0拒绝', () => {
    const onSubmit = vi.fn()
    render(<ExpenseForm members={members} onSubmit={onSubmit} />)

    fireEvent.change(screen.getByPlaceholderText('0.00'), {
      target: { value: '0' },
    })
    fireEvent.click(screen.getByLabelText('小王'))
    fireEvent.click(screen.getByText('添加'))

    expect(onSubmit).not.toHaveBeenCalled()
    expect(screen.getByText('金额必须大于 0')).toBeInTheDocument()
  })

  it('金额为负拒绝', () => {
    const onSubmit = vi.fn()
    render(<ExpenseForm members={members} onSubmit={onSubmit} />)

    fireEvent.change(screen.getByPlaceholderText('0.00'), {
      target: { value: '-100' },
    })
    fireEvent.click(screen.getByLabelText('小王'))
    fireEvent.click(screen.getByText('添加'))

    expect(onSubmit).not.toHaveBeenCalled()
    expect(screen.getByText('金额必须大于 0')).toBeInTheDocument()
  })

  it('参与人为空拒绝', () => {
    const onSubmit = vi.fn()
    render(<ExpenseForm members={members} onSubmit={onSubmit} />)

    fireEvent.change(screen.getByPlaceholderText('例如：酒店'), {
      target: { value: '酒店' },
    })
    fireEvent.change(screen.getByPlaceholderText('0.00'), {
      target: { value: '900' },
    })

    fireEvent.click(screen.getByText('添加'))

    expect(onSubmit).not.toHaveBeenCalled()
    expect(screen.getByText('至少选择一个参与人')).toBeInTheDocument()
  })
})
