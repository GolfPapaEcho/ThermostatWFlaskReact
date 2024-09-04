npx create-react-app thermostat-frontend
cd thermostat-frontend
npm install axios

App.js

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [currentTemperature, setCurrentTemperature] = useState(null);
  const [setpoint, setSetpoint] = useState('');
  const [newSetpoint, setNewSetpoint] = useState('');

  useEffect(() => {
    fetchTemperature();
    const interval = setInterval(fetchTemperature, 5000); // Fetch temperature every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchTemperature = async () => {
    try {
      const response = await axios.get('http://<RPI_IP_ADDRESS>:5000/api/temperature');
      setCurrentTemperature(response.data.current_temperature);
      setSetpoint(response.data.setpoint);
    } catch (error) {
      console.error('Error fetching temperature:', error);
    }
  };

  const handleSetpointChange = (e) => {
    setNewSetpoint(e.target.value);
  };

  const handleSetpointSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://<RPI_IP_ADDRESS>:5000/api/setpoint', {
        setpoint: parseFloat(newSetpoint),
      });
      setSetpoint(newSetpoint);
      setNewSetpoint('');
    } catch (error) {
      console.error('Error setting setpoint:', error);
    }
  };

  return (
    <div className="App">
      <h1>Thermostat Control</h1>
      <p>Current Temperature: {currentTemperature ? `${currentTemperature.toFixed(2)} °C` : 'Loading...'}</p>
      <p>Setpoint: {setpoint} °C</p>
      <form onSubmit={handleSetpointSubmit}>
        <input
          type="number"
          value={newSetpoint}
          onChange={handleSetpointChange}
          placeholder="Enter new setpoint"
        />
        <button type="submit">Set Setpoint</button>
      </form>
    </div>
  );
}

export default App;

