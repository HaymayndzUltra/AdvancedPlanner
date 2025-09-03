import { Link, Route, Routes } from 'react-router-dom'
import './App.css'
import Checkout from './pages/Checkout'
import OrderHistory from './pages/OrderHistory'

function App() {
	return (
		<div>
			<nav aria-label="Main Navigation">
				<Link to="/">Checkout</Link> | <Link to="/orders">Order History</Link>
			</nav>
			<Routes>
				<Route path="/" element={<Checkout />} />
				<Route path="/orders" element={<OrderHistory />} />
			</Routes>
		</div>
	)
}

export default App
