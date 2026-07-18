import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import './i18n'
import { ThemeProvider } from './context/ThemeContext.jsx'
import { MotionPreferenceProvider } from './context/MotionPreferenceContext.jsx'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ThemeProvider>
      <MotionPreferenceProvider>
        <App />
      </MotionPreferenceProvider>
    </ThemeProvider>
  </React.StrictMode>,
)
