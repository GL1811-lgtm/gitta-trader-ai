import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

// 🛡️ SECURITY: Ensure no Service Workers are running in Dev Mode
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.getRegistrations().then((registrations) => {
    registrations.forEach((registration) => {
      console.log('❌ Unregistering Service Worker:', registration);
      registration.unregister();
    });
  });
}

const rootElement = document.getElementById('root');
if (!rootElement) {
  throw new Error("Could not find root element to mount to");
}

const root = ReactDOM.createRoot(rootElement);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
