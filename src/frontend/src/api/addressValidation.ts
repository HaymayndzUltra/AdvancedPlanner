export type Address = {
	line1: string
	line2?: string
	city: string
	state: string
	postalCode: string
	country: string
}

export type AddressValidationResult = {
	isValid: boolean
	message?: string
	suggestions?: Partial<Address>[]
}

// Stubbed API to simulate async validation without sending PII to logs
export async function validateAddress(address: Address): Promise<AddressValidationResult> {
	await new Promise((r) => setTimeout(r, 50))
	const postalOk = /\d{5}(-\d{4})?/.test(address.postalCode)
	if (!postalOk) {
		return {
			isValid: false,
			message: 'Postal code format looks off. Example: 12345 or 12345-6789',
			suggestions: [
				{
					postalCode: '12345',
				},
			],
		}
	}
	return { isValid: true }
}

