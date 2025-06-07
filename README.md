# Distro V1 - Water Utility Management Platform

Distro V1 is a comprehensive digital twin platform designed for water utilities to manage infrastructure, maintenance operations, and customer service functions. Built with a multi-tenancy architecture, it enables water utilities to visualize, monitor, and maintain their water distribution networks while efficiently responding to customer needs through an intuitive web and mobile interface.

## Features
- **Multi-Tenancy**: Isolated schemas for each water utility.
- **Infrastructure Management**: Track assets, pipes, valves, meters, and zones with GIS support.
- **Customer Support**: Manage customer accounts, tickets, notifications, and service outages.
- **Maintenance**: Handle issues, maintenance tasks, and work orders.
- **User Management**: Role-based access control with location tracking for field agents.
- **Asynchronous Tasks**: Celery for background tasks like daily reports and asset checks.
- **API-Driven**: RESTful API with JWT authentication.

## Tech Stack
- **Backend**: Django, Django REST Framework, Django Tenants
- **Database**: PostgreSQL with PostGIS
- **Task Queue**: Celery with Redis
- **GIS**: GeoDjango for spatial data
- **Authentication**: JWT via `djangorestframework_simplejwt`

## Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL with PostGIS
- Redis
- Virtual environment
- Africa's Talking account (for SMS, optional)

### Installation
To be Updated