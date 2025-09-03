import { render, screen } from '@testing-library/react'
import OrderHistory from '../../src/pages/OrderHistory'

describe('OrderHistory', () => {
	it('renders initial orders and shows end message eventually', async () => {
		render(<OrderHistory />)
		const firstItemCandidates = await screen.findAllByText(/^Order #1 — \$10\.00$/)
		expect(firstItemCandidates[0]).toBeInTheDocument()
	})
})

