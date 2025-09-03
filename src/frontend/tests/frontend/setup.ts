import '@testing-library/jest-dom'

// Minimal IntersectionObserver polyfill for jsdom
class MockIntersectionObserver {
	callback: IntersectionObserverCallback
	constructor(callback: IntersectionObserverCallback) {
		this.callback = callback
	}
	observe() {
		// Immediately trigger with isIntersecting=true to simulate visibility
		this.callback([
			{
				isIntersecting: true,
				intersectionRatio: 1,
				target: ({} as unknown) as Element,
				boundingClientRect: ({} as unknown) as DOMRectReadOnly,
				intersectionRect: ({} as unknown) as DOMRectReadOnly,
				rootBounds: null,
				time: Date.now(),
			},
		] as unknown as IntersectionObserverEntry[], this as unknown as IntersectionObserver)
	}
	unobserve() {}
	disconnect() {}
}

// @ts-expect-error jsdom lacks this
global.IntersectionObserver = MockIntersectionObserver as unknown as typeof IntersectionObserver

