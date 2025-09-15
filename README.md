# TikTok Database API

A production-grade FastAPI backend with SQLAlchemy ORM for managing TikTok-related data including search topics, explore topics, user management, and more.

## Features

- **FastAPI** with automatic API documentation
- **SQLAlchemy ORM** with PostgreSQL/MySQL support
- **JWT Authentication** with role-based access control
- **Alembic** database migrations
- **Comprehensive testing** with pytest
- **Production-ready** configuration and security

## Project Structure

```
backend/
├── app/
│   ├── core/           # Configuration, database, security, roles
│   ├── models/         # SQLAlchemy ORM models
│   ├── schemas/        # Pydantic models
│   ├── crud/          # Database queries and logic
│   ├── api/           # API routes (versioned, modular)
│   └── utils/         # Helper functions and seeders
├── tests/             # Pytest tests
├── alembic/           # Database migrations
├── main.py           # FastAPI application entry point
└── requirements.txt  # Python dependencies
```

## Database Models

- **User** - User accounts with role-based permissions
- **Role** - User roles (admin, editor, viewer)
- **SearchTopic** - TikTok search topics with popularity metrics
- **SearchDetails** - Detailed information for each search topic
- **ScriptScenes** - Video script scenes for search topics
- **RelatedVideos** - Related videos for each search topic
- **ExploreTopics** - Independent explore topics

## API Endpoints

### Authentication (`/api/v1/auth`)

- `POST /login` - User login
- `POST /register` - User registration
- `GET /me` - Get current user info
- `POST /refresh` - Refresh access token

### Users (`/api/v1/users`)

- `GET /` - Get all users (admin only)
- `GET /me` - Get current user profile
- `GET /{user_id}` - Get user by ID (admin only)
- `POST /` - Create user (admin only)
- `PUT /{user_id}` - Update user profile
- `DELETE /{user_id}` - Delete user (admin only)
- `GET /roles/` - Get all roles (admin only)
- `POST /roles/` - Create role (admin only)

### Search (`/api/v1/search`)

- `GET /topics` - Get all search topics
- `POST /topics` - Create search topic (editor+)
- `GET /topics/{id}` - Get search topic by ID
- `PUT /topics/{id}` - Update search topic (editor+)
- `DELETE /topics/{id}` - Delete search topic (admin only)
- `GET /topics/search` - Search topics by title
- `GET /details/{topic_id}` - Get search details
- `POST /details/{topic_id}` - Create search details (editor+)
- And more endpoints for scenes and related videos...

### Explore (`/api/v1/explore`)

- `GET /topics` - Get all explore topics
- `POST /topics` - Create explore topic (editor+)
- `GET /topics/{id}` - Get explore topic by ID
- `PUT /topics/{id}` - Update explore topic (editor+)
- `DELETE /topics/{id}` - Delete explore topic (admin only)
- `GET /topics/trending` - Get trending topics
- `GET /topics/search` - Search explore topics

## Setup and Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd tiktok-database/backend
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**

   ```bash
   cp env.example .env
   # Edit .env with your database credentials
   ```

5. **Set up database**

   ```bash
   # Create database (PostgreSQL example)
   createdb tiktok_db

   # Run migrations
   alembic upgrade head
   ```

6. **Run the application**
   ```bash
   python main.py
   # Or with uvicorn directly:
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## Testing

Run the test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=app tests/
```

## Database Migrations

Create a new migration:

```bash
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:

```bash
alembic upgrade head
```

Rollback migrations:

```bash
alembic downgrade -1
```

## Role-Based Access Control

The API implements three user roles:

- **Admin**: Full access to all endpoints, can manage users and roles
- **Editor**: Can create/update content (search topics, explore topics, etc.)
- **Viewer**: Read-only access to most endpoints

## Environment Variables

Key environment variables (see `env.example`):

- `DATABASE_URL` - PostgreSQL connection string
- `DATABASE_URL_MYSQL` - MySQL connection string
- `DATABASE_TYPE` - Database type (postgresql or mysql)
- `SECRET_KEY` - JWT secret key
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time
- `ENVIRONMENT` - Environment (development/production)
- `DEBUG` - Enable debug mode

## API Documentation

Once the server is running, visit:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Security Features

- Password hashing with bcrypt
- JWT token authentication
- Role-based access control
- CORS protection
- Input validation with Pydantic
- SQL injection protection via SQLAlchemy ORM

## Production Deployment

For production deployment:

1. Set `ENVIRONMENT=production` and `DEBUG=false`
2. Use a strong `SECRET_KEY`
3. Configure proper database credentials
4. Set up reverse proxy (nginx)
5. Use process manager (systemd, supervisor, etc.)
6. Enable SSL/TLS
7. Set up monitoring and logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request
