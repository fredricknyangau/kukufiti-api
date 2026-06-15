-- Migration: 001_create_finance_tables.sql
-- Module: finance
-- Purpose: Create all database objects required by the finance module.
--
-- This migration is idempotent: every statement uses IF NOT EXISTS so that
-- re-running the file after a partial failure does not raise errors.
-- Applied migrations are tracked in public.schema_migrations by run_migration.py.

-- -------------------------------------------------------------------------
-- Schema
-- -------------------------------------------------------------------------
-- Ensure the finance schema exists. This guard makes the migration safe to
-- run against a fresh database (where init_db.sql may not have been executed)
-- as well as against an existing one where the schema was created by init_db.sql.
-- The finance_app role is granted USAGE on this schema by init_db.sql.
CREATE SCHEMA IF NOT EXISTS finance;

-- -------------------------------------------------------------------------
-- Extension
-- -------------------------------------------------------------------------
-- pgcrypto provides gen_random_uuid() used as the default for UUID primary keys.
-- Safe to enable multiple times (IF NOT EXISTS). On PostgreSQL 13+ the function
-- is a built-in, but enabling the extension is harmless on those versions.
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- -------------------------------------------------------------------------
-- Table: finance.transactions
-- -------------------------------------------------------------------------
-- Records every financial transaction associated with a batch: income from
-- bird sales and expenses (feed, medication, labour, etc.).
-- One row = one transaction event recorded by the farmer or the system.
CREATE TABLE IF NOT EXISTS finance.transactions (
    -- id: UUID primary key generated server-side. UUIDs prevent sequential ID
    -- enumeration (IDOR) and allow client-side ID generation for offline-first
    -- workflows in future mobile clients.
    id               UUID          PRIMARY KEY DEFAULT gen_random_uuid(),

    -- batch_id: foreign key to the batch this transaction belongs to.
    -- Stored as UUID (not a FK constraint) because the finance schema's
    -- application role (finance_app) has no cross-schema FK privileges to
    -- batches.batches. Cross-module referential integrity is enforced at the
    -- application layer (the finance service verifies the batch exists before
    -- inserting). This is a deliberate trade-off to maintain schema isolation.
    batch_id         UUID          NOT NULL,

    -- transaction_type: direction of the money flow.
    --   income:  money received (e.g. sale of birds, manure, eggs).
    --   expense: money spent (e.g. feed, day-old chicks, veterinary costs).
    -- CHECK constraint ensures only these two values are stored.
    transaction_type TEXT          NOT NULL
                                   CHECK (transaction_type IN ('income', 'expense')),

    -- category: sub-classification of the transaction within its type.
    -- Free-text (not an enum) to allow flexibility as new categories emerge
    -- without requiring a migration. Example values: "feed", "medication",
    -- "bird_sale", "labour", "transport".
    category         TEXT          NOT NULL,

    -- amount_kes: transaction value in Kenyan Shillings (KES).
    -- NUMERIC(12,2): up to 9,999,999,999.99 KES — sufficient for any realistic
    -- farm transaction. NUMERIC avoids floating-point precision loss that
    -- would occur with FLOAT or DOUBLE PRECISION for monetary arithmetic.
    -- CHECK (amount_kes > 0) enforces a positive amount; the direction
    -- (income vs expense) is captured by transaction_type, not the sign.
    amount_kes       NUMERIC(12,2) NOT NULL CHECK (amount_kes > 0),

    -- mpesa_reference: the M-Pesa transaction reference number (e.g. "QHX7Y83LPM").
    -- NULL for non-M-Pesa transactions (cash, bank transfer, etc.).
    -- When present, can be used to cross-reference with the mpesa_requests table.
    mpesa_reference  TEXT,

    -- transaction_date: the business date of the transaction (DATE, not TIMESTAMPTZ).
    -- DATE is used because the farmer cares about which day a purchase was made,
    -- not the exact time. Defaults to CURRENT_DATE (server's date in UTC) if
    -- not provided by the client.
    transaction_date DATE          NOT NULL DEFAULT CURRENT_DATE,

    -- notes: optional free-text notes for the transaction (e.g. "Paid to Kamau").
    notes            TEXT,

    -- status: payment/processing status of the transaction.
    --   pending:   payment initiated but not yet confirmed (e.g. M-Pesa STK push sent).
    --   confirmed: payment successfully received and verified.
    --   failed:    payment attempt failed (e.g. M-Pesa timeout, insufficient funds).
    -- Defaults to 'confirmed' for manually entered transactions where payment
    -- is assumed to have already occurred.
    status           TEXT          NOT NULL DEFAULT 'confirmed'
                                   CHECK (status IN ('pending', 'confirmed', 'failed')),

    -- created_at: row creation timestamp in UTC.
    -- Not updated on changes (use a separate updated_at column if mutation tracking is needed).
    created_at       TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);

-- -------------------------------------------------------------------------
-- Table: finance.mpesa_requests
-- -------------------------------------------------------------------------
-- Tracks M-Pesa STK Push (Lipa na M-Pesa) payment requests and their outcomes.
-- One row = one STK Push initiation. Linked to finance.transactions once confirmed.
--
-- FLOW:
--   1. Client requests payment → app initiates STK Push → creates mpesa_requests row (pending).
--   2. M-Pesa sends a callback → app updates status to 'completed' or 'failed'.
--   3. On 'completed': app creates a finance.transactions row and optionally
--      links it back via transaction_id.
CREATE TABLE IF NOT EXISTS finance.mpesa_requests (
    -- id: UUID primary key for internal references.
    id                    UUID          PRIMARY KEY DEFAULT gen_random_uuid(),

    -- transaction_id: optional FK to finance.transactions once the payment is confirmed.
    -- NULL while the request is pending or if it failed without creating a transaction.
    -- References the same schema so a proper FK constraint is safe here.
    transaction_id        UUID          REFERENCES finance.transactions(id),

    -- checkout_request_id: the unique ID assigned by the M-Pesa API to this STK Push.
    -- Used to match the callback from M-Pesa (which includes this ID) to the correct
    -- request row. UNIQUE ensures no duplicate callbacks are processed.
    checkout_request_id   TEXT          NOT NULL UNIQUE,

    -- merchant_request_id: another M-Pesa-assigned ID returned in the STK Push response.
    -- Stored for debugging and audit purposes; not used for matching callbacks.
    merchant_request_id   TEXT          NOT NULL,

    -- phone_number: the customer's Safaricom phone number that received the STK Push.
    -- Stored in international format (e.g. "+254712345678" or "254712345678").
    phone_number          TEXT          NOT NULL,

    -- amount_kes: the amount requested in the STK Push (must match the transaction amount).
    -- NUMERIC(12,2) for consistency with finance.transactions.amount_kes.
    amount_kes            NUMERIC(12,2) NOT NULL,

    -- status: current state of the M-Pesa request.
    --   pending:   STK Push sent, waiting for customer to enter PIN and M-Pesa to callback.
    --   completed: M-Pesa confirmed the payment (ResultCode = 0 in callback).
    --   failed:    Payment failed (e.g. wrong PIN, timeout, insufficient balance).
    --   cancelled: Customer cancelled the STK Push prompt.
    status                TEXT          NOT NULL DEFAULT 'pending'
                                        CHECK (status IN ('pending','completed','failed','cancelled')),

    -- mpesa_receipt_number: the M-Pesa confirmation code (e.g. "QHX7Y83LPM").
    -- Only present after a successful payment. NULL until status = 'completed'.
    -- This is the same value stored in finance.transactions.mpesa_reference.
    mpesa_receipt_number  TEXT,

    -- result_code: the numeric result code from M-Pesa's callback (0 = success).
    -- Stored to allow debugging payment failures without re-querying M-Pesa.
    result_code           INTEGER,

    -- result_desc: the human-readable result description from M-Pesa's callback.
    -- Examples: "The service request is processed successfully.",
    --           "Request cancelled by user."
    result_desc           TEXT,

    -- created_at: when the STK Push was initiated.
    created_at            TIMESTAMPTZ   NOT NULL DEFAULT NOW(),

    -- completed_at: when the callback was received and the request was finalised.
    -- NULL until the M-Pesa callback arrives (status changes from pending).
    completed_at          TIMESTAMPTZ
);

-- -------------------------------------------------------------------------
-- Indexes
-- -------------------------------------------------------------------------

-- idx_transactions_batch_id: speeds up queries that filter transactions by batch.
-- The most common query pattern for the finance module is
--     WHERE batch_id = $1
-- (e.g. "show all income and expenses for batch X"). Without this index,
-- every such query would perform a full table scan.
CREATE INDEX IF NOT EXISTS idx_transactions_batch_id
    ON finance.transactions(batch_id);

-- idx_transactions_batch_type: composite index for queries filtered by both
-- batch and transaction type (e.g. "show all expenses for batch X").
-- PostgreSQL can use this index for queries that filter on batch_id alone
-- (leftmost prefix), and also for queries that filter on both batch_id AND
-- transaction_type. This index makes the "income vs expense breakdown per batch"
-- query fast without a separate index on transaction_type.
CREATE INDEX IF NOT EXISTS idx_transactions_batch_type
    ON finance.transactions(batch_id, transaction_type);

-- idx_mpesa_checkout_id: unique index on checkout_request_id.
-- The UNIQUE constraint on the column already creates an implicit index, but
-- declaring it explicitly with IF NOT EXISTS makes this migration safely
-- re-runnable without "index already exists" errors on PostgreSQL versions
-- that do not support `CREATE UNIQUE INDEX IF NOT EXISTS` via the constraint.
-- Used to look up a request row when an M-Pesa callback arrives.
CREATE INDEX IF NOT EXISTS idx_mpesa_checkout_id
    ON finance.mpesa_requests(checkout_request_id);

-- idx_mpesa_status: partial index on pending M-Pesa requests.
-- A background job that polls for timed-out requests (status = 'pending'
-- older than N minutes) uses this index. The partial condition
-- (WHERE status = 'pending') means the index only includes pending rows —
-- completed and failed rows are excluded, keeping the index small and
-- minimising write overhead as most requests eventually become non-pending.
CREATE INDEX IF NOT EXISTS idx_mpesa_status
    ON finance.mpesa_requests(status)
    WHERE status = 'pending';
