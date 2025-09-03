import { trackEvent } from '../../src/telemetry/events'

describe('telemetry trackEvent', () => {
	it('redacts likely PII fields', async () => {
		const calls: any[] = []
		// @ts-expect-error override
		global.fetch = async (_url: string, init?: RequestInit) => {
			calls.push(JSON.parse(String(init?.body)))
			return new Response()
		}
		await trackEvent('test', {
			address: '123 Main',
			city: 'Springfield',
			postalCode: '12345',
			other: 'ok',
		})
		expect(calls[0].props.address).toBe('[REDACTED]')
		expect(calls[0].props.city).toBe('[REDACTED]')
		expect(calls[0].props.postalCode).toBe('[REDACTED]')
		expect(calls[0].props.other).toBe('ok')
	})
})

