import React, { useState, useEffect } from 'react';
import { getTrashCount } from '../services/api';

const TrashCount = () => {
  const [trashCount, setTrashCount] = useState(0);

  useEffect(() => {
    const fetchTrashCount = async () => {
      try {
        const count = await getTrashCount();
        setTrashCount(count);
      } catch (error) {
        console.error('Failed to fetch trash count:', error);
      }
    };

    fetchTrashCount();
  }, []);

  return (
    <div>
      <h2>Trash Count</h2>
      <p>Total Trash Detected: {trashCount}</p>
    </div>
  );
};

export default TrashCount;
