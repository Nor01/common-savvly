import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

import { UsersProvider } from './contexts/UsersContext';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <UsersProvider>
    <App />
  </UsersProvider>
);
