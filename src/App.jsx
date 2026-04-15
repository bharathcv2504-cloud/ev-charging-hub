import { useState, useEffect } from 'react'

function App() {
  const [activeTab, setActiveTab] = useState('finder')

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif', maxWidth: '600px', margin: '0 auto' }}>
      <h1 style={{ textAlign: 'center' }}>⚡ EV Charging Hub</h1>
      
      {/* Navigation Menu */}
      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px', justifyContent: 'center' }}>
        <button onClick={() => setActiveTab('finder')} style={tabStyle(activeTab === 'finder')}>Find Stations</button>
        <button onClick={() => setActiveTab('simulator')} style={tabStyle(activeTab === 'simulator')}>Charging Simulator</button>
        <button onClick={() => setActiveTab('calculator')} style={tabStyle(activeTab === 'calculator')}>Calculator</button>
      </div>

      {/* Tab Content */}
      {activeTab === 'finder' && <StationFinder />}
      {activeTab === 'simulator' && <ChargingSimulator />}
      {activeTab === 'calculator' && <Calculator />}
    </div>
  )
}

// --- TAB 1: STATION FINDER ---
// --- TAB 1: STATION FINDER ---
function StationFinder() {
  const [placeName, setPlaceName] = useState("Bengaluru") 
  const [stations, setStations] = useState([])
  const [loading, setLoading] = useState(false)

  const findStations = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://localhost:8000/api/chargers/nearby', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ place_name: placeName }) // Send the string instead of lat/lng
      })
      const data = await response.json()
      setStations(data)
    } catch (error) {
      console.error("Error fetching stations:", error)
    }
    setLoading(false)
  }

  return (
    <div style={cardStyle}>
      <h2>Nearby Stations</h2>
      <p style={{ fontSize: '12px', color: 'gray' }}>Mock cities: Bengaluru, Mysuru, Chennai</p>
      <div style={{ display: 'flex', gap: '10px', marginBottom: '15px' }}>
        <input 
          type="text" 
          value={placeName} 
          onChange={e => setPlaceName(e.target.value)} 
          placeholder="Enter city name..."
          style={{ padding: '8px', flex: 1, borderRadius: '4px', border: '1px solid #ccc' }}
        />
        <button onClick={findStations} disabled={loading} style={{ padding: '8px 16px', cursor: 'pointer' }}>
          {loading ? "Searching..." : "Find"}
        </button>
      </div>

      {stations.length > 0 ? stations.map(station => (
        <div key={station.id} style={{ padding: '10px', border: '1px solid #ccc', marginBottom: '10px', borderRadius: '5px' }}>
          <strong>{station.name}</strong> ({station.distance_km} km away)
          <p style={{ margin: '5px 0', fontSize: '14px' }}>Rate: {station.charge_rate_kw}kW | Cost: ${station.cost_per_kwh}/kWh</p>
          <span style={{ color: station.status === 'Available' ? 'green' : 'red', fontWeight: 'bold', fontSize: '14px' }}>{station.status}</span>
        </div>
      )) : (
        <p style={{ color: '#666' }}>Click find to search for stations.</p>
      )}
    </div>
  )
}

// --- TAB 2: CHARGING SIMULATOR ---
function ChargingSimulator() {
  const [sessionId, setSessionId] = useState(null)
  const [sessionData, setSessionData] = useState(null)

  // Poll the backend every 2 seconds if we have an active session
  useEffect(() => {
    let interval;
    if (sessionId) {
      interval = setInterval(async () => {
        const res = await fetch(`http://localhost:8000/api/sessions/${sessionId}`)
        if (res.ok) {
          const data = await res.json()
          setSessionData(data)
          if (data.status !== "ACTIVE") clearInterval(interval)
        }
      }, 2000)
    }
    return () => clearInterval(interval)
  }, [sessionId])

  const startSession = async () => {
    const res = await fetch('http://localhost:8000/api/sessions/start?user_id=u1&station_id=s1', { method: 'POST' })
    const data = await res.json()
    setSessionId(data.session.id)
    setSessionData(data.session)
  }

  const stopSession = async () => {
    await fetch(`http://localhost:8000/api/sessions/stop/${sessionId}`, { method: 'POST' })
    setSessionId(null)
  }

  return (
    <div style={cardStyle}>
      <h2>Live Charging Session</h2>
      <p style={{ fontSize: '14px', color: '#666' }}>Using mock User (Alice) and Station (Downtown Fast Charger).</p>
      
      {!sessionData || sessionData.status !== "ACTIVE" ? (
        <button onClick={startSession} style={{ padding: '10px 20px', background: '#28a745', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>Start Charging</button>
      ) : (
        <button onClick={stopSession} style={{ padding: '10px 20px', background: '#dc3545', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>Stop Charging</button>
      )}

      {sessionData && (
        <div style={{ marginTop: '20px', background: '#e9ecef', padding: '15px', borderRadius: '8px' }}>
          <h3>Status: {sessionData.status}</h3>
          <p><strong>Energy Delivered:</strong> {sessionData.kwh_delivered.toFixed(4)} kWh</p>
          <p><strong>Cost Incurred:</strong> ${sessionData.cost_incurred.toFixed(4)}</p>
        </div>
      )}
    </div>
  )
}

// --- TAB 3: CALCULATOR ---
function Calculator() {
  const [calc, setCalc] = useState({ battery_capacity_kwh: 50, current_percentage: 20, target_percentage: 80, charge_rate_kw: 50, cost_per_kwh: 0.50 })
  const [result, setResult] = useState(null)

  const handleCalculate = async () => {
    const response = await fetch('http://localhost:8000/api/chargers/calculate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(calc)
    })
    setResult(await response.json())
  }

  return (
    <div style={cardStyle}>
      <h2>EV Calculator</h2>
      <div style={{ display: 'grid', gap: '10px' }}>
        <label>Battery Capacity (kWh): <input type="number" value={calc.battery_capacity_kwh} onChange={e => setCalc({...calc, battery_capacity_kwh: parseFloat(e.target.value)})} /></label>
        <label>Current %: <input type="number" value={calc.current_percentage} onChange={e => setCalc({...calc, current_percentage: parseFloat(e.target.value)})} /></label>
        <label>Target %: <input type="number" value={calc.target_percentage} onChange={e => setCalc({...calc, target_percentage: parseFloat(e.target.value)})} /></label>
        <label>Charge Rate (kW): <input type="number" value={calc.charge_rate_kw} onChange={e => setCalc({...calc, charge_rate_kw: parseFloat(e.target.value)})} /></label>
        <button onClick={handleCalculate} style={{ padding: '10px', cursor: 'pointer' }}>Calculate Estimate</button>
      </div>
      {result && (
        <div style={{ marginTop: '15px', padding: '10px', background: '#f8f9fa', borderRadius: '5px' }}>
          <p><strong>Time:</strong> {result.estimated_time_hours} hours</p>
          <p><strong>Cost:</strong> ${result.total_cost}</p>
        </div>
      )}
    </div>
  )
}

// --- UI STYLES ---
const tabStyle = (isActive) => ({
  padding: '10px 20px',
  cursor: 'pointer',
  background: isActive ? '#007bff' : '#f8f9fa',
  color: isActive ? 'white' : 'black',
  border: '1px solid #dee2e6',
  borderRadius: '5px',
  fontWeight: isActive ? 'bold' : 'normal'
})

const cardStyle = {
  background: 'white',
  padding: '20px',
  borderRadius: '8px',
  boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
  border: '1px solid #eaeaea'
}

export default App