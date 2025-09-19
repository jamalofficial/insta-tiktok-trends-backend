@echo off
REM Windows batch script for database migrations
REM Usage: migrate.bat [command] [options]

python migrate.py %*
