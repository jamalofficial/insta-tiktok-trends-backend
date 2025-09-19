#!/usr/bin/env python3
"""
Database Migration Management Script

This script provides convenient commands for managing database migrations.
It wraps Alembic commands and provides additional functionality.
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description=""):
    """Run a command and handle errors"""
    print(f"🔄 {description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ {description} failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False
    return True


def migrate_up():
    """Run all pending migrations"""
    return run_command("alembic upgrade head", "Running database migrations")


def migrate_down():
    """Rollback to previous migration"""
    return run_command("alembic downgrade -1", "Rolling back one migration")


def migrate_reset():
    """Reset database to base (removes all tables)"""
    print("⚠️  WARNING: This will delete ALL data in the database!")
    confirm = input("Are you sure you want to continue? (yes/no): ")
    if confirm.lower() == 'yes':
        return run_command("alembic downgrade base", "Resetting database to base")
    else:
        print("❌ Migration reset cancelled")
        return False


def migrate_status():
    """Show current migration status"""
    return run_command("alembic current", "Checking migration status")


def migrate_history():
    """Show migration history"""
    return run_command("alembic history", "Showing migration history")


def create_migration(message):
    """Create a new migration"""
    if not message:
        message = input("Enter migration message: ")
    return run_command(f'alembic revision --autogenerate -m "{message}"', f"Creating migration: {message}")


def main():
    parser = argparse.ArgumentParser(description="Database Migration Management")
    parser.add_argument("command", choices=[
        "up", "down", "reset", "status", "history", "create"
    ], help="Migration command to run")
    parser.add_argument("-m", "--message", help="Migration message (for create command)")
    
    args = parser.parse_args()
    
    # Change to project directory
    project_root = Path(__file__).parent
    import os
    os.chdir(project_root)
    
    if args.command == "up":
        success = migrate_up()
    elif args.command == "down":
        success = migrate_down()
    elif args.command == "reset":
        success = migrate_reset()
    elif args.command == "status":
        success = migrate_status()
    elif args.command == "history":
        success = migrate_history()
    elif args.command == "create":
        success = create_migration(args.message)
    else:
        print(f"❌ Unknown command: {args.command}")
        success = False
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
