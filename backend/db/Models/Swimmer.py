import logging
import psycopg2

logger = logging.getLogger(__name__)    

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
