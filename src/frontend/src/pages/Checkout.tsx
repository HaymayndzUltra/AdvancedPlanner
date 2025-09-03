import { useEffect, useMemo, useState } from 'react'
import { PaymentMethodSelector } from '../components/PaymentMethodSelector'
import type { PaymentMethod } from '../components/PaymentMethodSelector'
import { validateAddress } from '../api/addressValidation'
import type { Address } from '../api/addressValidation'
import { trackEvent } from '../telemetry/events'

type AddressErrors = Partial<Record<keyof Address, string>> & { form?: string }

export default function Checkout() {
	const [paymentMethod, setPaymentMethod] = useState<PaymentMethod>('card')
	const [address, setAddress] = useState<Address>({ line1: '', city: '', state: '', postalCode: '', country: '' })
	const [errors, setErrors] = useState<AddressErrors>({})
	const [isValidating, setIsValidating] = useState(false)
	const canSubmit = useMemo(() => {
		return !!address.line1 && !!address.city && !!address.state && !!address.postalCode && !!address.country
	}, [address])

	useEffect(() => {
		setErrors((e) => ({ ...e, form: undefined }))
	}, [paymentMethod])

	async function onValidateAddress() {
		setIsValidating(true)
		setErrors({})
		const result = await validateAddress(address)
		setIsValidating(false)
		if (!result.isValid) {
			setErrors({ form: result.message })
			trackEvent('address_validation_failed', { reason: result.message, postalCode: address.postalCode })
		}
	}

	function onChange<K extends keyof Address>(key: K, value: Address[K]) {
		setAddress((prev) => ({ ...prev, [key]: value }))
	}

	return (
		<div>
			<h1>Checkout</h1>
			<section aria-label="Payment Method">
				<PaymentMethodSelector value={paymentMethod} onChange={setPaymentMethod} />
			</section>

			<section aria-label="Shipping Address">
				<div role="group" aria-labelledby="addr-label">
					<h2 id="addr-label">Shipping Address</h2>
					<label>
						<span>Address line 1</span>
						<input aria-label="Address line 1" value={address.line1} onChange={(e) => onChange('line1', e.target.value)} />
					</label>
					<label>
						<span>Address line 2 (optional)</span>
						<input aria-label="Address line 2" value={address.line2 ?? ''} onChange={(e) => onChange('line2', e.target.value)} />
					</label>
					<label>
						<span>City</span>
						<input aria-label="City" value={address.city} onChange={(e) => onChange('city', e.target.value)} />
					</label>
					<label>
						<span>State</span>
						<input aria-label="State" value={address.state} onChange={(e) => onChange('state', e.target.value)} />
					</label>
					<label>
						<span>Postal Code</span>
						<input aria-label="Postal Code" value={address.postalCode} onChange={(e) => onChange('postalCode', e.target.value)} />
					</label>
					<label>
						<span>Country</span>
						<input aria-label="Country" value={address.country} onChange={(e) => onChange('country', e.target.value)} />
					</label>
					{errors.form ? (
						<p role="alert" aria-live="assertive">{errors.form}</p>
					) : null}
					<button onClick={onValidateAddress} disabled={!canSubmit || isValidating}>
						{isValidating ? 'Validating…' : 'Validate address'}
					</button>
				</div>
			</section>

			<button disabled={!canSubmit}>Place order</button>
		</div>
	)
}

