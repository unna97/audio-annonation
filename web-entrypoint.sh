#!/bin/bash
set -e

# Function to wait for PostgreSQL
wait_for_postgres() {
    echo "Waiting for PostgreSQL..."
    until PGPASSWORD=$DB_PASSWORD psql -h "db" -U "$DB_USER" -d "$DB_NAME" -c '\q' 2>/dev/null; do
        echo "PostgreSQL is unavailable - sleeping"
        sleep 1
    done
    echo "PostgreSQL is up"
}

# Wait for PostgreSQL to be ready
wait_for_postgres

# Start the main application
exec "$@"