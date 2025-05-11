#!/bin/bash

# Stop and remove containers
docker-compose down

# Drop and recreate database
sudo -u postgres psql <<EOF
DROP DATABASE IF EXISTS distro;
CREATE DATABASE distro OWNER distro;
\c distro
CREATE EXTENSION postgis;
EOF

# Remove migration files
rm -rf distro_backend/distro/migrations/*
rm -rf distro_backend/tenants/migrations/*

echo "Database reset complete. Run 'docker-compose up --build' to start."