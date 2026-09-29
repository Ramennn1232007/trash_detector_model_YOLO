import React, { useState, useEffect } from 'react';
import { getTrashCount } from '../services/api';

const WS_URL = (process.env.REACT_APP_API_URL || 'http://localhost:8000').replace(/^http/, 'ws') + '/ws/trash-count';

const TrashCount = () => {
  const [trashCount, setTrashCount] = useState(null);
  const [live, setLive] = useState(false);

  useEffect(() => {
    let socket;
    let pollTimer;

    const poll = async () => {
      try {
        setTrashCount(await getTrashCount());
      } catch (error) {
        console.error('Failed to fetch trash count:', error);
      }
    };

    try {
      socket = new WebSocket(WS_URL);
      socket.onopen = () => setLive(true);
      socket.onmessage = (e) => setTrashCount(JSON.parse(e.data).count);
      socket.onclose = () => {
        setLive(false);
        pollTimer = setInterval(poll, 3000); // fall back to polling if the socket drops
      };
    } catch {
      pollTimer = setInterval(poll, 3000);
    }
    poll();

    return () => {
      if (socket) socket.close();
      clearInterval(pollTimer);
    };
  }, []);

  return (
    <div>
      <h2>Trash Count</h2>
      <p>Total trash detected: {trashCount === null ? '...' : trashCount}</p>
      <p style={{ fontSize: '0.8em' }}>{live ? 'Live' : 'Polling every 3s'}</p>
    </div>
  );
};

export default TrashCount;
