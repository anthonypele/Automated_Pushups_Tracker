import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import path from 'path';
import { fileURLToPath } from 'url';
import pg from 'pg';

const { Pool } = pg;
const app = express();
const port = Number(process.env.PORT || 3001);
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

app.use(cors());
app.use(express.json());

const pool = process.env.DATABASE_URL
  ? new Pool({
      connectionString: process.env.DATABASE_URL,
      ssl: process.env.DATABASE_SSL === 'false' ? false : { rejectUnauthorized: false }
    })
  : null;

app.get('/api/health', (_req, res) => {
  res.json({ ok: true });
});

app.get('/api/pushups', async (req, res) => {
  if (!pool) {
    return res.status(500).json({ error: 'DATABASE_URL is not configured.' });
  }

  const pusher = typeof req.query.pusher === 'string' ? req.query.pusher.trim() : '';
  const params = [];
  let whereClause = '';

  if (pusher) {
    params.push(pusher);
    whereClause = 'WHERE name = $1';
  }

  try {
    const { rows } = await pool.query(
      `
        SELECT
          date,
          time,
          name AS pusher,
          pushups
        FROM pushups
        ${whereClause}
        ORDER BY date DESC, time DESC
      `,
      params
    );

    res.json({ records: rows });
  } catch (error) {
    console.error('Failed to fetch pushups:', error);
    res.status(500).json({ error: 'Failed to fetch pushup records.' });
  }
});

const distPath = path.join(__dirname, '..', 'dist');
app.use(express.static(distPath));
app.get('*', (_req, res) => {
  res.sendFile(path.join(distPath, 'index.html'));
});

app.listen(port, () => {
  console.log(`Pushups API listening on http://localhost:${port}`);
});
