import React, { useState, useEffect } from 'react';
import { getStatus } from '../services/api';

const Status = () => {
  const [status, setStatus] = useState('Loading...');

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const status = await getStatus();
        setStatus(status);
      } catch (error) {
        console.error('Failed to fetch status:', error);
      }
    };

    fetchStatus();
  }, []);

  return (
    <div>
      <h2>System Status</h2>
      <p>{status}</p>
    </div>
  );
};

export default Status;
