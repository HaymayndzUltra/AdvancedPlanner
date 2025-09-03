import { onCLS, onFCP, onINP, onLCP, onTTFB } from 'web-vitals'
import type { Metric } from 'web-vitals'

type TelemetrySink = (metric: Metric) => void

const postMetric: TelemetrySink = (metric) => {
	try {
		// Replace with real endpoint or analytics provider
		// Ensure no PII is sent; only performance metrics and anonymized context
		fetch('/telemetry', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			keepalive: true,
			body: JSON.stringify({
				name: metric.name,
				id: metric.id,
				value: metric.value,
				at: Date.now(),
			}),
		}).catch(() => {})
	} catch {
		// no-op
	}
}

export function registerWebVitals(): void {
	onCLS(postMetric)
	onFCP(postMetric)
	onINP(postMetric)
	onLCP(postMetric)
	onTTFB(postMetric)
}

