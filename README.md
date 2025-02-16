# URL Shortener Service

Django-based URL shortening service with public and private redirect capabilities, JWT authentication, and comprehensive API.

## Features

- JWT Authentication for API access
- Public and private URL redirects
- User management through Django admin
- RESTful API for redirect rule management
- Docker containerization
- Comprehensive test coverage
- PostgreSQL database

## Technical Stack

- Python 3.10+
- Django 5.1.6
- Django REST Framework 3.15.2
- PostgreSQL 15
- JWT Authentication
- Docker & Docker Compose

## Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd redirect-service
```

2. For a working project create `.env` file with required environment variables:

   (as this is a test project to save time .env is present )
```env
POSTGRES_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
DJANGO_SETTINGS_MODULE=redirect_service.settings.local
SECRET_KEY=your-secret-key
DEBUG=1
```

3. Build and run with Docker Compose:
```bash
docker-compose up --build
```

4. Create a superuser:
```bash
docker-compose exec web python manage.py createsuperuser
```

## API Endpoints

### Authentication
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token

### User Management
- `GET /api/users/` - List users (admin sees all, users see only themselves)

### Redirect Rules Management
- `GET /api/redirects/url/` - List all redirect rules
- `POST /api/redirects/url/` - Create new redirect rule
- `GET /api/redirects/url/{identifier}/` - Get specific redirect rule
- `PATCH /api/redirects/url/{identifier}/` - Update redirect rule
- `DELETE /api/redirects/url/{identifier}/` - Delete redirect rule

### Redirect Endpoints
- `GET /redirect/public/{identifier}/` - Public redirect
- `GET /redirect/private/{identifier}/` - Private redirect (requires authentication)

## API Usage Examples

### 1. Create New Redirect
```bash
curl -X POST \
-H "Authorization: Bearer {your-jwt-token}" \
-H "Content-Type: application/json" \
-d '{
    "redirect_url": "https://google.com",
    "is_private": false
}' \
http://localhost:8000/api/redirects/url/
```

### 2. List All Redirects
```bash
curl -X GET \
-H "Authorization: Bearer {your-jwt-token}" \
http://localhost:8000/api/redirects/url/
```

### 3. Use Public Redirect
```bash
curl -I http://localhost:8000/redirect/public/{identifier}
```

### 4. Use Private Redirect
```bash
curl -I \
-H "Authorization: Bearer {your-jwt-token}" \
http://localhost:8000/redirect/private/{identifier}
```

### 5. Update Redirect
```bash
curl -X PATCH \
-H "Authorization: Bearer {your-jwt-token}" \
-H "Content-Type: application/json" \
-d '{
    "is_private": true
}' \
http://localhost:8000/api/redirects/url/{identifier}
```

### 6. Delete Redirect
```bash
curl -X DELETE \
-H "Authorization: Bearer {your-jwt-token}" \
http://localhost:8000/api/redirects/url/{identifier}
```

## Project Structure

```
redirect_service/
├── apps/
│   ├── users/          # User management module
│   └── redirects/      # URL shortening and redirect functionality
├── redirect_service/   # Core project settings
├── tests/             # Test suite
└── docker-compose.yml
```

## Testing

Run the test suite:
```bash
docker-compose exec web pytest
```

## License

This project is licensed under the MIT License.