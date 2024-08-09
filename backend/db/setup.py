import psycopg2
from psycopg2 import sql
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def connect():
    try:
        conn = psycopg2.connect(
            dbname="swimmer-app",
            user="abene",
            password="98741",
            host="127.0.0.1",
            port="5432"
        )
        return conn
    except psycopg2.Error as e:
        logger.error(f"Unable to connect to the database: {e}")
        return None

def create_tables(conn):
    commands = (
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            club_id INTEGER,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS clubs (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL,
            city VARCHAR(255),
            owner_id INTEGER REFERENCES users(id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS swimmers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            year_of_birth INTEGER,
            gender VARCHAR(10),
            club_id INTEGER REFERENCES clubs(id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS championships (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            date DATE NOT NULL,
            location VARCHAR(255)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS events (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            distance INTEGER NOT NULL,
            stroke VARCHAR(50) NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS results (
            id SERIAL PRIMARY KEY,
            swimmer_id INTEGER REFERENCES swimmers(id),
            championship_id INTEGER REFERENCES championships(id),
            event_id INTEGER REFERENCES events(id),
            time INTERVAL NOT NULL,
            place INTEGER,
            points INTEGER
        );
        """
    )
    try:
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
        logger.info("Tables created successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f"Error creating tables: {error}")

def delete_user(conn, user_id):
    """
    Delete a user from the database.

    This function performs the following actions:
    1. Deletes the club owned by the user (if any)
    2. Sets club_id to NULL for any swimmers associated with the user's club
    3. Deletes the user

    Args:
    conn: Database connection object
    user_id: ID of the user to be deleted

    Returns:
    bool: True if the user was successfully deleted, False otherwise
    """
    try:
        cur = conn.cursor()

        # Delete the club owned by the user
        cur.execute("DELETE FROM clubs WHERE owner_id = %s", (user_id,))

        # Set club_id to NULL for swimmers associated with the user's club
        cur.execute("UPDATE swimmers SET club_id = NULL WHERE club_id IN (SELECT id FROM clubs WHERE owner_id = %s)", (user_id,))

        # Delete the user
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))

        affected_rows = cur.rowcount
        conn.commit()
        cur.close()

        if affected_rows > 0:
            logger.info(f"User with ID {user_id} deleted successfully.")
            return True
        else:
            logger.warning(f"No user found with ID {user_id}.")
            return False

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f"Error deleting user: {error}")
        conn.rollback()
        return False


def insert_user(conn, email, password_hash):
    sql = """
    INSERT INTO users (email, password_hash)
    VALUES (%s, %s)
    RETURNING id
    """
    try:
        cur = conn.cursor()
        cur.execute(sql, (email, password_hash))
        user_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        logger.info(f"User inserted successfully. ID: {user_id}")
        return user_id
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f"Error inserting user: {error}")
        return None

def insert_club(conn, club_name, city, owner_id):
    sql = """
    INSERT INTO clubs (name, city, owner_id)
    VALUES (%s, %s, %s)
    RETURNING id
    """
    try:
        cur = conn.cursor()
        cur.execute(sql, (club_name, city, owner_id))
        club_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        logger.info(f"Club inserted successfully. ID: {club_id}")
        return club_id
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f"Error inserting club: {error}")
        return None

def get_user_by_email(conn, email):
    sql = "SELECT id, email, password_hash FROM users WHERE email = %s"
    try:
        cur = conn.cursor()
        cur.execute(sql, (email,))
        user = cur.fetchone()
        cur.close()
        return user
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f"Error retrieving user: {error}")
        return None

def insert_swimmer(conn, swimmer_data):
    sql = """
    INSERT INTO swimmers (name, club, category, year_of_birth, event, time, place, points, championship)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id
    """
    try:
        cur = conn.cursor()
        cur.execute(sql, (
            swimmer_data['name'],
            swimmer_data['year_of_birth']
        ))
        swimmer_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        logger.info(f"Swimmer inserted successfully. ID: {swimmer_id}")
        return swimmer_id
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f"Error inserting swimmer: {error}")
        return None

def get_swimmer(conn, swimmer_id):
    sql = "SELECT * FROM swimmers WHERE id = %s"
    try:
        cur = conn.cursor()
        cur.execute(sql, (swimmer_id,))
        swimmer = cur.fetchone()
        cur.close()
        return swimmer
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f"Error retrieving swimmer: {error}")
        return None

def update_swimmer(conn, swimmer_id, swimmer_data):
    sql = """
    UPDATE swimmers
    SET name = %s, club = %s, category = %s, year_of_birth = %s,
        event = %s, time = %s, place = %s, points = %s, championship = %s
    WHERE id = %s
    """
    try:
        cur = conn.cursor()
        cur.execute(sql, (
            swimmer_data['name'],
            swimmer_data['club'],
            swimmer_data['category'],
            swimmer_data['year_of_birth'],
            swimmer_data['event'],
            swimmer_data['time'],
            swimmer_data['place'],
            swimmer_data['points'],
            swimmer_data['championship'],
            swimmer_id
        ))
        conn.commit()
        cur.close()
        logger.info(f"Swimmer updated successfully. ID: {swimmer_id}")
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f"Error updating swimmer: {error}")
        return False

if __name__ == "__main__":
    conn = connect()
    if conn is not None:
        create_tables(conn)
        conn.close()
    else:
        logger.error("Failed to connect to the database.")