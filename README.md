# TikTok Trends Backend

A Python backend API for managing TikTok trend exploration topics and their search results.

## Database Schema

### ExploreTopic Table
- `id`: Integer, Primary Key
- `topic`: String (255 chars)
- `origin_user_id`: Integer (ID of the user who added the topic)
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

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables in `.env` file

3. Run the application:
```bash
python -m app.main
```

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check

## Database Support

- MySQL (default)
- PostgreSQL

The application automatically creates tables on startup.
