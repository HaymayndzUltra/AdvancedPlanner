import { defineConfig } from 'vitest/config'

export default defineConfig({
	test: {
		environment: 'jsdom',
		setupFiles: ['tests/frontend/setup.ts'],
		globals: true,
		include: ['tests/frontend/**/*.test.ts', 'tests/frontend/**/*.test.tsx'],
	},
	esbuild: {
		jsx: 'automatic',
		jsxImportSource: 'react',
	},
	server: {
		fs: { allow: ['..', '/workspace'] },
	},
	coverage: {
		provider: 'v8',
		reports: ['text', 'html'],
		all: false,
		exclude: ['src/App.tsx', 'src/main.tsx', 'src/telemetry/webVitals.ts'],
		thresholds: {
			lines: 0.8,
			functions: 0.8,
			branches: 0.8,
			statements: 0.8,
		},
	},
})

