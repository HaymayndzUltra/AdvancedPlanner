import { useId } from 'react'

export type PaymentMethod = 'card' | 'paypal' | 'bank'

type Props = {
	value: PaymentMethod
	onChange: (next: PaymentMethod) => void
}

export function PaymentMethodSelector({ value, onChange }: Props) {
	const groupId = useId()
	return (
		<fieldset aria-labelledby={`${groupId}-label`}>
			<legend id={`${groupId}-label`}>Payment Method</legend>
			<div role="radiogroup" aria-labelledby={`${groupId}-label`}>
				<label>
					<input
						type="radio"
						name="payment-method"
						value="card"
						checked={value === 'card'}
						onChange={() => onChange('card')}
					/>
					<span aria-live="polite">Credit/Debit Card</span>
				</label>
				<label>
					<input
						type="radio"
						name="payment-method"
						value="paypal"
						checked={value === 'paypal'}
						onChange={() => onChange('paypal')}
					/>
					<span>PayPal</span>
				</label>
				<label>
					<input
						type="radio"
						name="payment-method"
						value="bank"
						checked={value === 'bank'}
						onChange={() => onChange('bank')}
					/>
					<span>Bank Transfer</span>
				</label>
			</div>
		</fieldset>
	)
}

