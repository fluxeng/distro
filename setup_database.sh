#!/bin/bash

# PostgreSQL Database Setup Script for Distro V1
# Run this script to set up your PostgreSQL database with PostGIS extension

echo "Setting up PostgreSQL database for Distro V1..."

# Drop existing database and user if they exist
echo "Dropping existing database and user..."
sudo -u postgres psql -c "DROP DATABASE IF EXISTS distro_db;"
sudo -u postgres psql -c "DROP USER IF EXISTS distro_user;"

# Create database user
echo "Creating database user..."
sudo -u postgres createuser --createdb --createrole --login distro_user

# Set password for the user
echo "Setting user password..."
sudo -u postgres psql -c "ALTER USER distro_user PASSWORD 'your_secure_password';"

# Create the main database
echo "Creating database..."
sudo -u postgres createdb -O distro_user distro_db

# Enable PostGIS extension
echo "Enabling PostGIS extensions..."
sudo -u postgres psql -d distro_db -c "CREATE EXTENSION IF NOT EXISTS postgis;"
sudo -u postgres psql -d distro_db -c "CREATE EXTENSION IF NOT EXISTS postgis_topology;"

# Grant necessary permissions
echo "Granting permissions..."
sudo -u postgres psql -d distro_db -c "GRANT ALL PRIVILEGES ON DATABASE distro_db TO distro_user;"
sudo -u postgres psql -d distro_db -c "GRANT ALL ON SCHEMA public TO distro_user;"

echo "Database setup complete!"
echo "Database: distro_db"
echo "User: distro_user"
echo "PostGIS extensions enabled"

# Verify PostGIS installation
echo "Verifying PostGIS installation..."
sudo -u postgres psql -d distro_db -c "SELECT PostGIS_Version();"

echo ""
echo "✅ Fresh database created! You can now run:"
echo "   python manage.py makemigrations"
echo "   python manage.py migrate_schemas --shared"