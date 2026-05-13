--- Create module schemas
CREATE SCHEMA IF NOT EXISTS batches;
CREATE SCHEMA IF NOT EXISTS finance;
CREATE SCHEMA IF NOT EXISTS health;
CREATE SCHEMA IF NOT EXISTS auth;
CREATE SCHEMA IF NOT EXISTS core;

-- Create module roles
CREATE ROLE batches_app WITH LOGIN PASSWORD 'batches_dev';
CREATE ROLE finance_app WITH LOGIN PASSWORD 'finance_dev';
CREATE ROLE health_app WITH LOGIN PASSWORD 'health_dev';
CREATE ROLE auth_app WITH LOGIN PASSWORD 'auth_dev';
CREATE ROLE core_app WITH LOGIN PASSWORD 'core_dev';

-- Grant schema ownership
GRANT USAGE ON SCHEMA batches TO batches_app;
GRANT ALL ON SCHEMA batches TO batches_app;
GRANT USAGE ON SCHEMA finance TO finance_app;
GRANT ALL ON SCHEMA finance TO finance_app;
GRANT USAGE ON SCHEMA health TO health_app;
GRANT ALL ON SCHEMA health TO health_app;
GRANT USAGE ON SCHEMA auth TO auth_app;
GRANT ALL ON SCHEMA auth TO auth_app;
GRANT USAGE ON SCHEMA core TO core_app;
GRANT ALL ON SCHEMA core TO core_app;

-- All modules roles can write to core.outbox
GRANT USAGE ON SCHEMA core TO batches_app, finance_app,
health_app, auth_app;

-- Default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA batches
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO
batches_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA finance
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO
finance_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA health
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO
health_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA auth
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO
auth_app;
