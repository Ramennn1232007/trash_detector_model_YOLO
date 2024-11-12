import React from 'react';
import TrashCount from './components/TrashCount';
import Status from './components/Status';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Trash Detection System</h1>
        <Status />
        <TrashCount />
      </header>
    </div>
  );
}

export default App;
