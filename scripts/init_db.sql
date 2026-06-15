-- init_db.sql — One-time database initialisation script for kukufiti-api.
--
-- PURPOSE
-- -------
-- This script bootstraps a fresh PostgreSQL database with the schemas, roles,
-- and privilege structure that the application expects. It is idempotent and
-- safe to re-run (every statement uses IF NOT EXISTS or DO $$ BEGIN...END $$
-- guards).
--
-- WHEN TO RUN
-- -----------
-- Run this script ONCE against a new database (local dev, staging, production)
-- before running the migration runner. The migration runner (run_migration.py)
-- creates tables and indexes; this script creates the schemas, roles, and
-- privileges that the migration runner and application rely on.
--
-- HOW TO RUN
-- ----------
-- As the PostgreSQL superuser (e.g. the user set in DATABASE_URL):
--     psql -d kukufiti -f scripts/init_db.sql
-- Or via Docker Compose:
--     docker compose exec db psql -U postgres -d kukufiti -f /scripts/init_db.sql
--
-- SECURITY NOTE
-- -------------
-- The default passwords ("batches_dev", "finance_dev", etc.) are only
-- suitable for local development. In staging and production, create roles
-- with strong passwords and inject them via the BATCHES_DB_URL, FINANCE_DB_URL,
-- etc. environment variables without running this script.

-- =========================================================================
-- SECTION 1: Module Schemas
-- =========================================================================
-- One schema per module enforces data isolation at the database layer.
-- The application role for each module (e.g. batches_app) has DML privileges
-- ONLY on its own schema. This means a bug in the finance module literally
-- cannot query or modify batches data — the database connection will be
-- refused with a "permission denied for schema batches" error.
--
-- The schemas are:
--   batches:  broiler batch lifecycle and performance data.
--   finance:  transactions, M-Pesa requests, and financial summaries.
--   health:   health logs, medication records, and veterinary events.
--   auth:     user accounts, sessions, and access tokens.
--   core:     shared infrastructure (e.g. the transactional outbox table).
CREATE SCHEMA IF NOT EXISTS batches;
CREATE SCHEMA IF NOT EXISTS finance;
CREATE SCHEMA IF NOT EXISTS health;
CREATE SCHEMA IF NOT EXISTS auth;
CREATE SCHEMA IF NOT EXISTS core;

-- =========================================================================
-- SECTION 2: Migration Tracking Table
-- =========================================================================
-- The schema_migrations table is used by scripts/run_migration.py to track
-- which migration files have been applied. It lives in the public schema so
-- the superuser always has access regardless of which module schema is active.
--
-- (module, filename) UNIQUE: prevents duplicate tracking records. If the
-- migration runner crashes after applying a migration but before recording
-- it, re-running will detect the missing record and re-apply the file.
-- Migration SQL files must be idempotent (use IF NOT EXISTS) to tolerate this.
CREATE TABLE IF NOT EXISTS public.schema_migrations (
    id         SERIAL      PRIMARY KEY,
    module     TEXT        NOT NULL,
    filename   TEXT        NOT NULL,
    applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (module, filename)
);

-- =========================================================================
-- SECTION 3: Application Roles
-- =========================================================================
-- Each module has a dedicated PostgreSQL role used by the FastAPI application
-- to connect to the database. These roles are granted DML privileges ONLY on
-- their own schema — they cannot CREATE or ALTER tables, and cannot access
-- other modules' schemas.
--
-- WHY CREATE ROLE has no IF NOT EXISTS:
-- PostgreSQL does not support `CREATE ROLE IF NOT EXISTS` (added in PG 16
-- for some statements, but not universally). The DO $$ block pattern wraps
-- each CREATE ROLE in a conditional that checks pg_roles first, making
-- the operation idempotent on all supported PostgreSQL versions.
--
-- NOTE: The passwords here are development defaults. Replace them with strong
-- random passwords in any shared or production environment.
DO $$
BEGIN
    -- batches_app: application role for the batches module.
    -- Used by the BATCHES_DB_URL connection string in .env.
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'batches_app') THEN
        CREATE ROLE batches_app WITH LOGIN PASSWORD 'batches_dev';
    END IF;

    -- finance_app: application role for the finance module.
    -- Used by the FINANCE_DB_URL connection string in .env.
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'finance_app') THEN
        CREATE ROLE finance_app WITH LOGIN PASSWORD 'finance_dev';
    END IF;

    -- health_app: application role for the health module.
    -- Used by the HEALTH_DB_URL connection string in .env.
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'health_app') THEN
        CREATE ROLE health_app WITH LOGIN PASSWORD 'health_dev';
    END IF;

    -- auth_app: application role for the authentication module.
    -- Used by the AUTH_DB_URL connection string in .env.
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'auth_app') THEN
        CREATE ROLE auth_app WITH LOGIN PASSWORD 'auth_dev';
    END IF;

    -- core_app: application role for shared core schema access.
    -- Used for writing to core.outbox (transactional outbox pattern) and
    -- any other shared infrastructure tables.
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'core_app') THEN
        CREATE ROLE core_app WITH LOGIN PASSWORD 'core_dev';
    END IF;
END $$;

-- =========================================================================
-- SECTION 4: Schema-Level Privilege Grants
-- =========================================================================
-- GRANT USAGE ON SCHEMA gives a role the ability to reference objects
-- (tables, sequences, functions) inside a schema. Without USAGE, a role
-- with table-level SELECT privileges still cannot query the table because
-- it cannot "enter" the schema namespace.
--
-- USAGE alone does not grant SELECT/INSERT/UPDATE/DELETE on tables inside
-- the schema — those are granted separately via ALTER DEFAULT PRIVILEGES
-- in Section 5 and by specific GRANT statements in migrations.
GRANT USAGE ON SCHEMA batches TO batches_app;
GRANT USAGE ON SCHEMA finance TO finance_app;
GRANT USAGE ON SCHEMA health  TO health_app;
GRANT USAGE ON SCHEMA auth    TO auth_app;
GRANT USAGE ON SCHEMA core    TO core_app;

-- All module roles need USAGE on the core schema so they can write to
-- core.outbox as part of their own transactions (transactional outbox pattern).
-- Granting USAGE here does NOT give them SELECT/INSERT on core tables —
-- those are controlled by separate GRANT statements.
GRANT USAGE ON SCHEMA core TO batches_app, finance_app, health_app, auth_app;

-- =========================================================================
-- SECTION 5: Default Table and Sequence Privileges
-- =========================================================================
-- ALTER DEFAULT PRIVILEGES sets the privileges that PostgreSQL will
-- automatically apply to NEW objects created in a schema by a specific role.
-- Without this, a table created in the batches schema by the superuser would
-- have no grants to batches_app — the role could enter the schema (USAGE)
-- but could not query any tables.
--
-- WHY `FOR ROLE fred`?
-- ALTER DEFAULT PRIVILEGES applies to objects created by the specified role.
-- "fred" is the local superuser that runs the migration runner. In production
-- this must be updated to match the actual migration runner role (the role
-- named in DATABASE_URL). If omitted, the default privileges would only apply
-- to objects created by the current session user, which may not be consistent.
--
-- GRANT … ON TABLES:
-- SELECT, INSERT, UPDATE, DELETE (full DML) — the application role can
-- read and write data but cannot DROP, TRUNCATE, or ALTER any table.
--
-- GRANT … ON SEQUENCES:
-- USAGE and SELECT are needed for SERIAL columns: the application role
-- must call nextval() (USAGE) and currval() (SELECT) to generate and read
-- sequence values for auto-increment primary keys.

-- Batches schema privileges
ALTER DEFAULT PRIVILEGES FOR ROLE fred IN SCHEMA batches
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO batches_app;
ALTER DEFAULT PRIVILEGES FOR ROLE fred IN SCHEMA batches
    GRANT USAGE, SELECT ON SEQUENCES TO batches_app;

-- Finance schema privileges
ALTER DEFAULT PRIVILEGES FOR ROLE fred IN SCHEMA finance
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO finance_app;
ALTER DEFAULT PRIVILEGES FOR ROLE fred IN SCHEMA finance
    GRANT USAGE, SELECT ON SEQUENCES TO finance_app;

-- Health schema privileges
ALTER DEFAULT PRIVILEGES FOR ROLE fred IN SCHEMA health
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO health_app;
ALTER DEFAULT PRIVILEGES FOR ROLE fred IN SCHEMA health
    GRANT USAGE, SELECT ON SEQUENCES TO health_app;

-- Auth schema privileges
ALTER DEFAULT PRIVILEGES FOR ROLE fred IN SCHEMA auth
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO auth_app;
ALTER DEFAULT PRIVILEGES FOR ROLE fred IN SCHEMA auth
    GRANT USAGE, SELECT ON SEQUENCES TO auth_app;
