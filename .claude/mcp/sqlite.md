# SQLite MCP Server

**Package:** `@modelcontextprotocol/server-sqlite`  
**Primary users:** data-engineer

## Purpose

Provides read/write access to a local SQLite database used as the team's market data warehouse. The data-engineer uses it to store ingested price data, fundamental snapshots, portfolio positions, trade records, and computed risk metrics so other agents can query structured data without hitting external APIs on every request.

## Setup

No API key is required. Configure the database path in `.env`:

```
DB_PATH=./data/finance.db
```

If `DB_PATH` is not set, the server defaults to `./data/finance.db`. The `data/` directory is gitignored; the database file is local only.

The server is registered in `.mcp.json`:

```json
"sqlite": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-sqlite", "${DB_PATH:-./data/finance.db}"]
}
```

Initialize the database directory before first use:

```bash
mkdir -p data
```

## Tools Exposed

### `query`

Execute a read-only SELECT statement and return results as JSON rows.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sql` | string | yes | SELECT statement to execute |

### `execute`

Execute a write statement (INSERT, UPDATE, DELETE, CREATE, etc.) and return rows affected.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sql` | string | yes | SQL statement to execute |

### `list_tables`

Return the names of all tables in the database. No parameters required.

### `describe_table`

Return the column definitions (name, type, constraints) for a named table.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `table` | string | yes | Table name |

## Suggested Schema

The data-engineer should initialize the following tables on first setup:

### `prices`
```sql
CREATE TABLE IF NOT EXISTS prices (
    ticker      TEXT NOT NULL,
    date        TEXT NOT NULL,
    open        REAL,
    high        REAL,
    low         REAL,
    close       REAL,
    adj_close   REAL,
    volume      INTEGER,
    source      TEXT,
    fetched_at  TEXT DEFAULT (datetime('now')),
    PRIMARY KEY (ticker, date)
);
```

### `fundamentals`
```sql
CREATE TABLE IF NOT EXISTS fundamentals (
    ticker          TEXT NOT NULL,
    period_end      TEXT NOT NULL,
    period_type     TEXT NOT NULL,  -- 'annual' or 'quarterly'
    revenue         REAL,
    net_income      REAL,
    eps             REAL,
    pe_ratio        REAL,
    market_cap      REAL,
    source          TEXT,
    fetched_at      TEXT DEFAULT (datetime('now')),
    PRIMARY KEY (ticker, period_end, period_type)
);
```

### `positions`
```sql
CREATE TABLE IF NOT EXISTS positions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker          TEXT NOT NULL,
    quantity        REAL NOT NULL,
    avg_cost        REAL NOT NULL,
    market_value    REAL,
    as_of_date      TEXT NOT NULL,
    updated_at      TEXT DEFAULT (datetime('now'))
);
```

### `trades`
```sql
CREATE TABLE IF NOT EXISTS trades (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker          TEXT NOT NULL,
    trade_date      TEXT NOT NULL,
    side            TEXT NOT NULL,  -- 'buy' or 'sell'
    quantity        REAL NOT NULL,
    price           REAL NOT NULL,
    commission      REAL DEFAULT 0,
    notes           TEXT,
    created_at      TEXT DEFAULT (datetime('now'))
);
```

### `risk_metrics`
```sql
CREATE TABLE IF NOT EXISTS risk_metrics (
    ticker          TEXT NOT NULL,
    as_of_date      TEXT NOT NULL,
    var_95_1d       REAL,  -- 1-day 95% VaR
    var_99_1d       REAL,  -- 1-day 99% VaR
    cvar_95_1d      REAL,  -- Conditional VaR / Expected Shortfall
    beta            REAL,
    volatility_30d  REAL,
    sharpe_30d      REAL,
    computed_at     TEXT DEFAULT (datetime('now')),
    PRIMARY KEY (ticker, as_of_date)
);
```
