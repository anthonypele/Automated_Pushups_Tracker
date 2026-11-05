import React from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';

function formatDate(value) {
  if (!value) return '-';

  if (typeof value === 'string' && /^\d{4}-\d{2}-\d{2}/.test(value)) {
    return value.slice(0, 10);
  }

  return new Intl.DateTimeFormat(undefined, {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  }).format(new Date(value));
}

function formatTime(value) {
  if (!value) return '-';
  return String(value).slice(0, 8);
}

function App() {
  const [records, setRecords] = React.useState([]);
  const [pusherOptions, setPusherOptions] = React.useState([]);
  const [selectedPusher, setSelectedPusher] = React.useState('All');
  const [isLoading, setIsLoading] = React.useState(true);
  const [error, setError] = React.useState('');

  React.useEffect(() => {
    async function loadInitialRecords() {
      setIsLoading(true);
      setError('');

      try {
        const response = await fetch('/api/pushups');
        const payload = await response.json();

        if (!response.ok) {
          throw new Error(payload.error || 'Failed to load pushups.');
        }

        const nextRecords = payload.records || [];
        setRecords(nextRecords);
        setPusherOptions([...new Set(nextRecords.map((record) => record.pusher).filter(Boolean))].sort());
      } catch (loadError) {
        setError(loadError.message);
      } finally {
        setIsLoading(false);
      }
    }

    loadInitialRecords();
  }, []);

  React.useEffect(() => {
    if (selectedPusher === 'All') return;

    async function loadFilteredRecords() {
      setIsLoading(true);
      setError('');

      try {
        const params = new URLSearchParams({ pusher: selectedPusher });
        const response = await fetch(`/api/pushups?${params.toString()}`);
        const payload = await response.json();

        if (!response.ok) {
          throw new Error(payload.error || 'Failed to load pushups.');
        }

        setRecords(payload.records || []);
      } catch (loadError) {
        setError(loadError.message);
      } finally {
        setIsLoading(false);
      }
    }

    loadFilteredRecords();
  }, [selectedPusher]);

  async function handlePusherChange(event) {
    const nextPusher = event.target.value;
    setSelectedPusher(nextPusher);

    if (nextPusher !== 'All') return;

    setIsLoading(true);
    setError('');

    try {
      const response = await fetch('/api/pushups');
      const payload = await response.json();

      if (!response.ok) {
        throw new Error(payload.error || 'Failed to load pushups.');
      }

      setRecords(payload.records || []);
    } catch (loadError) {
      setError(loadError.message);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="app-shell">
      <aside className="sidebar" aria-label="Primary navigation">
        <a className="brand-link" href="/">
          Pushups
        </a>
      </aside>

      <main className="content">
        <div className="page-header">
          <div>
            <p className="eyebrow">Automated Pushups Tracker</p>
            <h1>Pushups</h1>
          </div>
        </div>

        <section className="toolbar" aria-label="Pushup filters">
          <label htmlFor="pusher">Pusher</label>
          <select id="pusher" value={selectedPusher} onChange={handlePusherChange}>
            <option value="All">All</option>
            {pusherOptions.map((pusher) => (
              <option key={pusher} value={pusher}>
                {pusher}
              </option>
            ))}
          </select>
        </section>

        {error ? <div className="status status-error">{error}</div> : null}
        {isLoading ? <div className="status">Loading pushups...</div> : null}

        {!isLoading && !error ? (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Time</th>
                  <th>Pusher</th>
                  <th className="numeric">Pushups</th>
                </tr>
              </thead>
              <tbody>
                {records.length ? (
                  records.map((record, index) => (
                    <tr key={`${record.date}-${record.time}-${record.pusher}-${index}`}>
                      <td>{formatDate(record.date)}</td>
                      <td>{formatTime(record.time)}</td>
                      <td>{record.pusher || '-'}</td>
                      <td className="numeric">{record.pushups ?? '-'}</td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td className="empty-state" colSpan="4">
                      No pushup records found.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        ) : null}
      </main>
    </div>
  );
}

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
