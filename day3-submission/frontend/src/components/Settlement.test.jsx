import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import Settlement from './Settlement'

const settlement = {
  totalAmount: 1340,
  members: [
    { name: '小王', paid: 900, shouldPay: 460, balance: 440 },
    { name: '小李', paid: 360, shouldPay: 420, balance: -60 },
    { name: '小张', paid: 80, shouldPay: 460, balance: -380 },
  ],
  transfers: [
    { from: '小张', to: '小王', amount: 380 },
    { from: '小李', to: '小王', amount: 60 },
  ],
}

describe('Settlement', () => {
  it('结果渲染', () => {
    render(<Settlement settlement={settlement} />)

    expect(screen.getByText('结算结果')).toBeInTheDocument()
    expect(screen.getByText('总支出：¥1340.00')).toBeInTheDocument()
    expect(screen.getByText('小王')).toBeInTheDocument()
    expect(screen.getByText('小李')).toBeInTheDocument()
    expect(screen.getByText('小张')).toBeInTheDocument()
    expect(screen.getByText(/小张 → 小王/)).toBeInTheDocument()
    expect(screen.getByText(/小李 → 小王/)).toBeInTheDocument()
  })

  it('余额颜色-正数', () => {
    render(<Settlement settlement={settlement} />)
    const positiveCell = screen.getByText('+440.00')
    expect(positiveCell).toHaveClass('positive')
  })

  it('余额颜色-负数', () => {
    render(<Settlement settlement={settlement} />)
    const negativeCell = screen.getByText('-60.00')
    expect(negativeCell).toHaveClass('negative')
  })
})
