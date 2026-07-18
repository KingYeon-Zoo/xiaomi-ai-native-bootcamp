import { BrowserRouter, Routes, Route } from 'react-router-dom'
import TripList from './pages/TripList'
import TripDetail from './pages/TripDetail'
import './App.css'
import './components/components.css'
import './pages/TripDetail.css'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<TripList />} />
        <Route path="/trips/:id" element={<TripDetail />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
