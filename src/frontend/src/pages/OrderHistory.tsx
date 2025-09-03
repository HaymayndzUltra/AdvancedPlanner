import { useEffect, useRef, useState } from 'react'

type Order = { id: string; totalCents: number }

async function fetchOrders(cursor?: string): Promise<{ items: Order[]; nextCursor?: string }> {
	await new Promise((r) => setTimeout(r, 40))
	const start = cursor ? parseInt(cursor, 10) : 0
	const pageSize = 10
	const items: Order[] = Array.from({ length: pageSize }, (_, i) => ({ id: String(start + i + 1), totalCents: 1000 + (start + i) * 50 }))
	const next = start + pageSize < 50 ? String(start + pageSize) : undefined
	return { items, nextCursor: next }
}

export default function OrderHistory() {
	const [orders, setOrders] = useState<Order[]>([])
	const [cursor, setCursor] = useState<string | undefined>(undefined)
	const [hasMore, setHasMore] = useState(true)
	const [isLoading, setIsLoading] = useState(false)
	const sentinelRef = useRef<HTMLDivElement | null>(null)
	const seenIdsRef = useRef<Set<string>>(new Set())

	useEffect(() => {
		loadMore()
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [])

	useEffect(() => {
		const node = sentinelRef.current
		if (!node) return
		const observer = new IntersectionObserver((entries) => {
			entries.forEach((entry) => {
				if (entry.isIntersecting && hasMore && !isLoading) {
					loadMore()
				}
			})
		})
		observer.observe(node)
		return () => observer.disconnect()
	}, [hasMore, isLoading])

	async function loadMore() {
		if (isLoading || !hasMore) return
		setIsLoading(true)
		const res = await fetchOrders(cursor)
		setOrders((prev) => {
			const newItems = res.items.filter((o) => !seenIdsRef.current.has(o.id))
			newItems.forEach((o) => seenIdsRef.current.add(o.id))
			return [...prev, ...newItems]
		})
		setCursor(res.nextCursor)
		setHasMore(Boolean(res.nextCursor))
		setIsLoading(false)
	}

	return (
		<div>
			<h1>Order History</h1>
			<ul aria-label="Orders list">
				{orders.map((o) => (
					<li key={o.id}>Order #{o.id} — ${(o.totalCents / 100).toFixed(2)}</li>
				))}
			</ul>
			<div ref={sentinelRef} aria-hidden="true" style={{ height: 1 }} />
			{!hasMore && <p>End of results</p>}
		</div>
	)
}

