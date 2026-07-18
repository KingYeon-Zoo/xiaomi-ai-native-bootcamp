import { render, screen, fireEvent } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import TripForm from './TripForm'

describe('TripForm', () => {
  it('创建成功', () => {
    const onSubmit = vi.fn()
    render(<TripForm onSubmit={onSubmit} />)

    fireEvent.change(screen.getByPlaceholderText('例如：南京 3 日游'), {
      target: { value: '南京游' },
    })
    const dateInputs = screen.getAllByDisplayValue('')
    fireEvent.change(dateInputs[0], { target: { value: '2026-07-01' } })
    fireEvent.change(dateInputs[1], { target: { value: '2026-07-03' } })

    fireEvent.click(screen.getByText('创建旅行'))

    expect(onSubmit).toHaveBeenCalledWith({
      name: '南京游',
      startDate: '2026-07-01',
      endDate: '2026-07-03',
    })
  })

  it('名称为空拒绝', () => {
    const onSubmit = vi.fn()
    render(<TripForm onSubmit={onSubmit} />)

    fireEvent.click(screen.getByText('创建旅行'))

    expect(onSubmit).not.toHaveBeenCalled()
    expect(screen.getByText('旅行名称不能为空')).toBeInTheDocument()
  })
})
