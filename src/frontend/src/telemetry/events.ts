type TelemetryEvent = {
	name: string
	props?: Record<string, unknown>
}

function sanitizeProps(props?: Record<string, unknown>): Record<string, unknown> | undefined {
	if (!props) return undefined
	const redacted: Record<string, unknown> = {}
	for (const [key, value] of Object.entries(props)) {
		// Best-effort PII filtering by key heuristics
		if (/address|line|city|state|postal|zip|country|name|email|phone/i.test(key)) {
			redacted[key] = '[REDACTED]'
		} else {
			redacted[key] = value
		}
	}
	return redacted
}

export async function trackEvent(name: string, props?: Record<string, unknown>): Promise<void> {
	const payload: TelemetryEvent = {
		name,
		props: sanitizeProps(props),
	}
	try {
		await fetch('/telemetry/events', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			keepalive: true,
			body: JSON.stringify(payload),
		})
	} catch {
		// swallow errors in client telemetry
	}
}

