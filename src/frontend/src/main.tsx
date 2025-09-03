import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import { registerWebVitals } from './telemetry/webVitals'
import App from './App.tsx'
import { BrowserRouter } from 'react-router-dom'

createRoot(document.getElementById('root')!).render(
	<StrictMode>
		<BrowserRouter>
			<App />
		</BrowserRouter>
	</StrictMode>,
)

registerWebVitals()
