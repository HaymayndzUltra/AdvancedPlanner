import { render, screen, fireEvent } from '@testing-library/react'
import Checkout from '../../src/frontend/src/pages/Checkout'

describe('Checkout Address Validation', () => {
	it('shows error when postal code invalid and clears when valid', async () => {
		render(<Checkout />)
		fireEvent.change(screen.getByLabelText('Address line 1'), { target: { value: '123 Main' } })
		fireEvent.change(screen.getByLabelText('City'), { target: { value: 'Springfield' } })
		fireEvent.change(screen.getByLabelText('State'), { target: { value: 'IL' } })
		fireEvent.change(screen.getByLabelText('Postal Code'), { target: { value: 'ABC' } })
		fireEvent.change(screen.getByLabelText('Country'), { target: { value: 'US' } })

		fireEvent.click(screen.getByRole('button', { name: /validate address/i }))
		expect(await screen.findByRole('alert')).toHaveTextContent('Postal code format looks off')

		fireEvent.change(screen.getByLabelText('Postal Code'), { target: { value: '12345' } })
		fireEvent.click(screen.getByRole('button', { name: /validate address/i }))
		await new Promise((r) => setTimeout(r, 60))
		expect(screen.queryByRole('alert')).toBeNull()
	})
})

