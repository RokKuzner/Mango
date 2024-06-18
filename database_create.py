from database import start_cassandra_session

def create_websites_db_if_not_exists():
  #Get the db session and wait for cassandra to be availible
  session, cluster = start_cassandra_session('cassandra', 9042)

  # Create keyspace
  session.execute("""
  CREATE KEYSPACE IF NOT EXISTS websites
  WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 1}
  """)

  # Use the keyspace
  session.set_keyspace('websites')

  #Make websites table
  session.execute("""
  CREATE TABLE IF NOT EXISTS websites (
    url text PRIMARY KEY,
    title text,
    keywords set<text>
  )
  """)

  #Make keywords table
  session.execute("""
  CREATE TABLE IF NOT EXISTS keywords (
    keyword text,
    url text,
    PRIMARY KEY (keyword, url)
  )
  """)

  #Make websites to crawl table
  session.execute("""
  CREATE TABLE IF NOT EXISTS tocrawl (
    url text PRIMARY KEY
  )
  """)

  session.shutdown()
  cluster.shutdown()