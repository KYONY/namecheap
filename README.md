# URL Shortener Service

A Django-based URL shortening service with public and private redirect capabilities.

## Features

- JWT Authentication
- Public and private URL redirects
- User management through Django admin
- RESTful API for redirect rule management
- Docker support

## Requirements

- Docker and Docker Compose
- Python 3.8+
- PostgreSQL

## Quick Start

1. Clone the repository
2. Run with Docker Compose:
```bash
docker-compose up --build
```

3. Create a superuser:
```bash
docker-compose exec web python manage.py createsuperuser
```

4. Get JWT token:
```bash
curl --request POST \
  --url http://localhost:8000/api/token/ \
  --data '{
    "username": "your_username",
    "password": "your_password"
}'
```

## API Endpoints

### Authentication
- POST /api/token/ - Obtain JWT token
- POST /api/token/refresh/ - Refresh JWT token

### Redirect Rules
- GET /api/urls/ - List all redirect rules (authenticated)
- POST /api/urls/ - Create new redirect rule (authenticated)
- GET /api/urls/{id}/ - Retrieve redirect rule (authenticated)
- PATCH /api/urls/{id}/ - Update redirect rule (authenticated, owner only)
- DELETE /api/urls/{id}/ - Delete redirect rule (authenticated, owner only)

### Redirects
- GET /redirect/public/{identifier}/ - Public redirect
- GET /redirect/private/{identifier}/ - Private redirect (requires authentication)

## Development

1. Install dependencies:
```bash
pipenv install
```

2. Run migrations:
```bash
python manage.py migrate
```

3. Run tests:
```bash
python manage.py test
```

## Project Structure

The project is organized into several modules:

- `core/` - Main project settings and configuration
- `users/` - User management and authentication
- `redirects/` - URL shortening and redirect functionality
- `tests/` - Unit tests

## License

MIT License
