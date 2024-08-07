#!/bin/bash
set -e

# start postgres:
/usr/local/bin/docker-entrypoint.sh postgres &


# Function to check if database exists
database_exists() {
    psql -U "$DB_USER" -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'" | grep -q 1
}

# Wait for PostgreSQL to be ready
until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"

# Create database if it doesn't exist
if ! database_exists; then
    PGPASSWORD=$DB_PASSWORD psql -U "$DB_USER" -d postgres -c "CREATE DATABASE \"$DB_NAME\";"
    echo "Database $DB_NAME created."
else
    echo "Database $DB_NAME already exists."
fi

# # Start the main application
# exec "$@"
wait

