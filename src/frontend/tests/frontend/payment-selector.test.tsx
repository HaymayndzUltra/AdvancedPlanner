import { render, screen, fireEvent } from '@testing-library/react'
import { PaymentMethodSelector } from '../../src/components/PaymentMethodSelector'

describe('PaymentMethodSelector accessibility', () => {
	it('allows selection with radio buttons and reflects state', () => {
		let value: any = 'card'
		const onChange = (v: any) => (value = v)
		render(<PaymentMethodSelector value={value} onChange={onChange} />)
		fireEvent.click(screen.getByLabelText('PayPal'))
		expect(value).toBe('paypal')
	})
})

