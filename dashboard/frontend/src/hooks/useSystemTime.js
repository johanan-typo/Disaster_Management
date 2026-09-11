import { useState, useEffect } from 'react';

/**
 * Hook providing dynamically updating system time from the client's laptop/browser clock.
 * Updates exactly every second using new Date().
 * Completely decoupled from simulation_time.
 */
export function useSystemTime() {
  const [timeState, setTimeState] = useState(() => {
    const now = new Date();
    return formatDateTime(now);
  });

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeState(formatDateTime(new Date()));
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  return timeState;
}

function formatDateTime(d) {
  // HH:MM:SS (24-hour format)
  const hours = String(d.getHours()).padStart(2, '0');
  const minutes = String(d.getMinutes()).padStart(2, '0');
  const seconds = String(d.getSeconds()).padStart(2, '0');
  const timeString = `${hours}:${minutes}:${seconds}`;

  // DD MMM YYYY (e.g. 09 Sep 2026)
  const day = String(d.getDate()).padStart(2, '0');
  const monthNames = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
  ];
  const month = monthNames[d.getMonth()];
  const year = d.getFullYear();
  const dateString = `${day} ${month} ${year}`;

  return {
    time: timeString,
    date: dateString,
    iso: d.toISOString(),
  };
}
