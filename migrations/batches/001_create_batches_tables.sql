-- This migration prepares the database objects used by app/modules/batches/repository.py.
-- Creating the schema first makes fresh database setup work reliably.
CREATE SCHEMA IF NOT EXISTS batches;

-- The batches.id default uses gen_random_uuid().
-- pgcrypto provides that function on PostgreSQL versions where it is not built in.
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS batches.batches (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    batch_name TEXT NOT NULL,
    breed      TEXT NOT NULL,
    quantity   INTEGER NOT NULL CHECK (quantity > 0),
    start_date DATE NOT NULL,
    end_date   DATE,
    status     TEXT NOT NULL DEFAULT 'active' CHECK (status IN
    ('active', 'closed', 'archived')),

    -- Performance metrics (updated via health logs)
    total_feed_kg  NUMERIC(10,2) NOT NULL DEFAULT 0,
    mortality_count INTEGER NOT NULL DEFAULT 0,

    -- Soft delete
    deleted_at  TIMESTAMPTZ,

    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_batches_status
   ON batches.batches(status)
   WHERE deleted_at IS NULL;

CREATE INDEX IF NOT EXISTS idx_batches_start_date
   ON batches.batches(start_date DESC)
   WHERE deleted_at IS NULL;
