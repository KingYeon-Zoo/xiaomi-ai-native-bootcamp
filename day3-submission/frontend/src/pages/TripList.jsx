import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { getTrips, createTrip } from '../api/trips'
import TripForm from '../components/TripForm'
import EmptyState from '../components/EmptyState'

function TripList() {
  const [trips, setTrips] = useState([])
  const [showForm, setShowForm] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    loadTrips()
  }, [])

  async function loadTrips() {
    const data = await getTrips()
    setTrips(data.trips || [])
  }

  async function handleCreate(tripData) {
    await createTrip(tripData)
    setShowForm(false)
    loadTrips()
  }

  return (
    <div className="trip-list-page">
      <header>
        <h1>TripSplit</h1>
        <button className="primary" onClick={() => setShowForm(true)}>新建旅行</button>
      </header>

      {showForm && (
        <TripForm onSubmit={handleCreate} />
      )}

      {trips.length === 0 && !showForm ? (
        <EmptyState message="还没有旅行，创建一个开始吧！" actionLabel="新建旅行" onAction={() => setShowForm(true)} />
      ) : (
        <div className="trip-cards">
          {trips.map((trip) => (
            <div key={trip.id} className="trip-card" onClick={() => navigate(`/trips/${trip.id}`)}>
              <h3>{trip.name}</h3>
              <p>{trip.startDate} ~ {trip.endDate}</p>
              <p>{trip.memberCount} 位成员 · {trip.expenseCount} 笔账单</p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default TripList
