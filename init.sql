-- ./init.sql

-- Safely create user and DB
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_catalog.pg_roles WHERE rolname = 'pokerMLUser'
    ) THEN
        CREATE USER pokerMLUser WITH PASSWORD 'MLWhisk777!';
    END IF;

    IF NOT EXISTS (
        SELECT FROM pg_database WHERE datname = 'pokerMLdb'
    ) THEN
        CREATE DATABASE pokerMLdb OWNER pokerMLUser;
    END IF;
END
$$;