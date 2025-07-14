-- 1. Create role if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_catalog.pg_roles WHERE rolname = 'pokermluser'
    ) THEN
        CREATE ROLE pokerMLUser LOGIN PASSWORD 'MLWhisk777!';
    END IF;
END
$$;

-- 2. Manually run CREATE DATABASE outside of a DO block
-- NOTE: This must be outside DO $$...$$
-- So run this manually, or run the full script with `psql` as superuser:

-- Make sure this line is outside any function block:
CREATE DATABASE pokerMLdb OWNER pokerMLUser;