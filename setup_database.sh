#!/bin/bash

# PostgreSQL Database Setup Script for Distro V1
# Run this script to set up your PostgreSQL database with PostGIS extension

echo "Setting up PostgreSQL database for Distro V1..."

# Create database user
sudo -u postgres createuser --createdb --createrole --login distro_user

# Set password for the user
sudo -u postgres psql -c "ALTER USER distro_user PASSWORD 'your_secure_password';"

# Create the main database
sudo -u postgres createdb -O distro_user distro_db

# Enable PostGIS extension
sudo -u postgres psql -d distro_db -c "CREATE EXTENSION IF NOT EXISTS postgis;"
sudo -u postgres psql -d distro_db -c "CREATE EXTENSION IF NOT EXISTS postgis_topology;"

# Grant necessary permissions
sudo -u postgres psql -d distro_db -c "GRANT ALL PRIVILEGES ON DATABASE distro_db TO distro_user;"
sudo -u postgres psql -d distro_db -c "GRANT ALL ON SCHEMA public TO distro_user;"

echo "Database setup complete!"
echo "Database: distro_db"
echo "User: distro_user"
echo "PostGIS extensions enabled"

# Verify PostGIS installation
echo "Verifying PostGIS installation..."
sudo -u postgres psql -d distro_db -c "SELECT PostGIS_Version();"
