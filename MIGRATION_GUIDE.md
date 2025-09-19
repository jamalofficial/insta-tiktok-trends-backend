# Database Migration Guide

This guide explains how to manage database migrations for the TikTok Trends Backend project.

## Overview

The project uses Alembic for database migrations, providing a clean and maintainable way to manage database schema changes.

## Migration Commands

### Using the Migration Script

The project includes a convenient migration script (`migrate.py`) that wraps Alembic commands:

```bash
# Run all pending migrations
python migrate.py up

# Rollback one migration
python migrate.py down

# Reset database (removes all tables - DANGEROUS!)
python migrate.py reset

# Check current migration status
python migrate.py status

# Show migration history
python migrate.py history

# Create a new migration
python migrate.py create -m "your migration message"
```

### Using Alembic Directly

You can also use Alembic commands directly:

```bash
# Run migrations
alembic upgrade head

# Rollback migrations
alembic downgrade -1

# Reset to base (removes all tables)
alembic downgrade base

# Check status
alembic current

# Show history
alembic history

# Create new migration
alembic revision --autogenerate -m "your message"
```

## Migration Files

Migration files are stored in `alembic/versions/` and follow this naming pattern:
- `{revision_id}_{description}.py`

### Current Migrations

1. **9cc42856d16a_drop_all_existing_tables** - Drops all existing tables to start fresh
2. **9bf32219cd35_create_explore_topic_and_topic_result_tables** - Creates the new database schema

## Database Schema

### ExploreTopic Table
- `id`: Integer, Primary Key
- `topic`: String (255 chars)
- `origin_user_id`: Integer
- `last_scrape`: DateTime (nullable)
- `created_at`: DateTime (auto-generated)
- `updated_at`: DateTime (auto-updated)

### TopicResult Table
- `id`: Integer, Primary Key
- `explore_id`: Foreign Key → ExploreTopic.id
- `relevant_keyword`: String (255 chars)
- `search_popularity`: Float (nullable)
- `search_increase`: Float (nullable)
- `location_data`: JSON (nullable)
- `demographic_data`: JSON (nullable)
- `time_period_7_days`: Date (nullable)
- `time_period_today`: Date (nullable)
- `created_at`: DateTime (auto-generated)
- `updated_at`: DateTime (auto-updated)

## Best Practices

1. **Always backup your database** before running migrations in production
2. **Test migrations** on a development database first
3. **Review migration files** before applying them
4. **Use descriptive migration messages**
5. **Never edit existing migration files** - create new ones instead

## Troubleshooting

### Migration Fails
If a migration fails:
1. Check the error message
2. Fix the issue in the migration file
3. Run the migration again

### Database Out of Sync
If the database is out of sync:
1. Check current status: `alembic current`
2. Check what migrations are available: `alembic history`
3. Run migrations: `alembic upgrade head`

### Reset Database
If you need to start completely fresh:
1. **WARNING: This deletes all data!**
2. Run: `alembic downgrade base`
3. Run: `alembic upgrade head`

## Development Workflow

1. Make changes to your models
2. Create a migration: `python migrate.py create -m "description"`
3. Review the generated migration file
4. Test the migration: `python migrate.py up`
5. Commit your changes

## Production Deployment

1. Backup the production database
2. Run migrations: `python migrate.py up`
3. Verify the migration was successful: `python migrate.py status`
4. Test the application

## Environment Variables

Make sure these environment variables are set in your `.env` file:

```env
DATABASE_TYPE=mysql
DATABASE_URL_MYSQL=mysql+pymysql://user:password@host:port/database
DATABASE_URL=postgresql://user:password@host:port/database
```
