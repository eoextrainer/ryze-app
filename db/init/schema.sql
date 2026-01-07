-- Core audit schema for RYZE change tracking
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(64) UNIQUE NOT NULL,
  password VARCHAR(128) NOT NULL,
  role VARCHAR(32) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS change_iterations (
  id SERIAL PRIMARY KEY,
  commit_hash VARCHAR(64) UNIQUE NOT NULL,
  message TEXT NOT NULL,
  branch VARCHAR(64) NOT NULL DEFAULT 'main',
  reason VARCHAR(128) NOT NULL DEFAULT 'fs-change',
  actor VARCHAR(128) NOT NULL DEFAULT 'auto',
  rollback_reference VARCHAR(64),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_change_iterations_created_at ON change_iterations (created_at DESC);
