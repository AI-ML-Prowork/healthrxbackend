# Multi-Tenant Application

This project is a multi-tenant Django application that supports user authentication, JWT token-based authentication, WebSocket notifications using Django Channels, and Elasticsearch integration for blogs. The application is designed with both public and tenant-specific schemas and incorporates a custom user model.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Configuration](#configuration)
- [Admin Panel and Tenant Based Admin Panel](#admin-panel-and-tenant-based-admin-panel)
- [WebSocket Notifications](#websocket-notifications)
- [Logging](#logging)
- [Elasticsearch Integration](#elasticsearch-integration)

---

## Features

- **Multi-Tenant Architecture**: Supports separate schemas for different tenants with shared apps and tenant-specific apps.
- **Custom User Model**: Uses a `CustomUser` model with tenant-level authentication and admin capabilities.
- **JWT Authentication**: Implements JWT token authentication for API security.
- **WebSocket Notifications**: Real-time notifications using Django Channels and WebSocket.
- **Blog Management**: Create, update, delete, and view blogs with tenant-based filtering.
- **Swagger API Documentation**: Auto-generated API documentation using `drf-yasg`.
- **Elasticsearch Integration**: Allows full-text search for blog posts.

## Technologies Used

- **Django**: Python web framework.
- **Django Rest Framework (DRF)**: For building REST APIs.
- **Django Channels**: For WebSocket communication.
- **PostgreSQL**: Database backend with multi-tenant support using `django-tenants`.
- **Elasticsearch**: Full-text search engine for blog content.
- **JWT**: JSON Web Tokens for authentication.
- **Swagger**: For API documentation.
- **Redis**: As a backend for Django Channels.

## Installation

1. Unzip


2. Create a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use venv\Scripts\activate
    ```

3. Install Elasticsearch from archive on Linux:

```
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.15.1-linux-x86_64.tar.gz
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.15.1-linux-x86_64.tar.gz.sha512
shasum -a 512 -c elasticsearch-8.15.1-linux-x86_64.tar.gz.sha512 
tar -xzf elasticsearch-8.15.1-linux-x86_64.tar.gz
cd elasticsearch-8.15.1/ 
```

4. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```



5. Set up your PostgreSQL database. Add your database credentials in the `.env` file:

    ```env
    SECRET_KEY=<your-secret-key>
    DATABASE_NAME=<your-database-name>
    DATABASE_USER=<your-database-user>
    DATABASE_PASSWORD=<your-database-password>
    DATABASE_HOST=<your-database-host>
    DATABASE_PORT=<your-database-port>
    REDIS_HOST=<your-redis-hostname/docker-service-name>
    ELASTIC_SEARCH_HOST=<your-es-hostname/docker-service-name>
    ```

6. Run the Redis server in docker:

    ```bash
    docker run -d --name redis -p 6379:6379

7. Create migrations:
```
python manage.py makemigrations
```

8. Migrate the migrations:
```
python manage.py migrate_schemas --shared

python manage.py migrate_schemas --tenant
```

9. Run the development server:

    ```bash
    python manage.py runserver
    ```

10. Websocket will be automatically managed through frontend.
11. (Optional) You can add below websocket request on postman to trigger notifications mannually:
    ```ws://127.0.0.1:8000/ws/notifications/?tenant_name=intel&query_string=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI2MDM0Nzg1LCJpYXQiOjE3MjU5NDgzODUsImp0aSI6IjhhOWJlZmY2ODc1NTQyZGY5MmUzNjViY2ZjNjI1MmRhIiwidXNlcl9pZCI6Mn0.FYcGXuboLibgBHWH9mEy343iXpVQ_nT7in9iGjUlI0A```

## Configuration

- **Django Settings**:
  - The application uses environment variables defined in `.env` to manage configurations like `SECRET_KEY`, `DATABASE` details, and `DEBUG` mode.
  - Multi-tenant configuration is handled through `django-tenants` in the settings.

- **JWT Token Settings**:
  JWT settings are defined in the `SIMPLE_JWT` configuration in `settings.py`.

- **Channel Layers**:
  For WebSocket connections, Redis is used as the channel layer backend. Ensure Redis is installed and running on your machine.


## Admin Panel

The Django admin panel can be accessed at `/admin/`:

- **Global Superuser**: Can manage all tenants.
- **Tenant Superuser**: Can manage their specific tenant.

To create a Global superuser for managing tenants:

#### Global Superuser
```bash
python manage.py createsuperuser
```

Now admin can login to Endpoint:
```
{host}/admin/
```
And can manage users and tenants

#### Tenant Superuser
While creating tenant the creds which was used to create tenant can be used to login for tenant superuser. 

Now Tenant admin can login to Endpoint:
```
{domain}.{localhost}/admin/
```
Tenant specific superuser can manage thier own users.


## WebSocket Notifications

- **Use case**: Admin can send real time notification using websocket to all the users with in the tenant

## Logging

- **Use case**: Logging are used to debug any potential error or current error, you can fing logs into:
```
debug.log
```

## Elasticsearch Integration

- **Use case**: User or tenant can simply search blogs with title and description using elastic search which includes instant searching.

We have isolated indexes for each tenant.