# Source package for Balaji Marble Arts website

"""
Database initialization script
Run this to initialize the database with sample data
Usage: python -m src
"""
from app import app
from src.database import init_database

def main():
    """Main function to initialize database"""
    print("Initializing database...")
    init_database(app)
    print("\n✅ Database initialization complete!")

if __name__ == '__main__':
    main()
