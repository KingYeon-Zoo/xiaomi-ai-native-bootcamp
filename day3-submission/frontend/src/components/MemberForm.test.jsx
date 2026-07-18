import { render, screen, fireEvent } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import MemberForm from './MemberForm'

describe('MemberForm', () => {
  it('添加成功', () => {
    const onSubmit = vi.fn()
    render(<MemberForm existingMembers={[]} onSubmit={onSubmit} />)

    fireEvent.change(screen.getByPlaceholderText('输入成员名'), {
      target: { value: '小王' },
    })
    fireEvent.click(screen.getByText('添加'))

    expect(onSubmit).toHaveBeenCalledWith({ name: '小王' })
  })

  it('空名拒绝', () => {
    const onSubmit = vi.fn()
    render(<MemberForm existingMembers={[]} onSubmit={onSubmit} />)

    fireEvent.click(screen.getByText('添加'))

    expect(onSubmit).not.toHaveBeenCalled()
    expect(screen.getByText('成员名不能为空')).toBeInTheDocument()
  })

  it('重复名拒绝', () => {
    const onSubmit = vi.fn()
    render(<MemberForm existingMembers={['小王']} onSubmit={onSubmit} />)

    fireEvent.change(screen.getByPlaceholderText('输入成员名'), {
      target: { value: '小王' },
    })
    fireEvent.click(screen.getByText('添加'))

    expect(onSubmit).not.toHaveBeenCalled()
    expect(screen.getByText('成员名已存在')).toBeInTheDocument()
  })
})
