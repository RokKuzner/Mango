import psycopg2
from psycopg2 import sql
import os

# Database connection parameters
db_params = {
  "dbname": os.getenv("DATABASE_NAME"),
  "user": os.getenv("DATABASE_USER"),
  "password": os.getenv("DATABASE_PASSWORD"),
  "host": os.getenv("DATABASE_HOST"),
  "port": os.getenv("DATABASE_PORT")
}

def create_tables():
  commands = (
    "CREATE EXTENSION IF NOT EXISTS pg_trgm;",
  
    """
    CREATE TABLE IF NOT EXISTS to_index (
      url VARCHAR(255) NOT NULL UNIQUE,
      timestamp_utc DOUBLE PRECISION NOT NULL
    );
    """,

    """
    CREATE TABLE IF NOT EXISTS keywords (
      keyword VARCHAR(255) NOT NULL UNIQUE 
    );
    """,
    "CREATE INDEX IF NOT EXISTS idx_keyword_trgm ON keywords USING GIN (keyword gin_trgm_ops);",

    """
    CREATE TABLE IF NOT EXISTS webpage_by_keyword (
      keyword VARCHAR(255) NOT NULL,
      url TEXT NOT NULL
    );
    """,
    "CREATE INDEX IF NOT EXISTS idx_keyword ON webpage_by_keyword(keyword)"

    """
    CREATE TABLE IF NOT EXISRS latest_website_crawl_time (
      url VARCHAR(138) PRIMARY KEY UNIQUE,
      timestamp_utc DOUBLE PRECISION NOT NULL
    );
    """,
    "CREATE INDEX IF NOT EXISTS idx_url ON latest_website_crawl_time(url)"
  )

  try:
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    # Create each table
    for command in commands:
        cursor.execute(command)

    # Commit the changes
    connection.commit()
    print("Tables created successfully")
  except (Exception, psycopg2.DatabaseError) as error:
    print(f"Error: {error}")
  finally:
    if connection is not None:
        cursor.close()
        connection.close()

if __name__ == "__main__":
  create_tables()