import logging
import psycopg2

logger = logging.getLogger(__name__)    

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

def delete_club(conn, club_id):
    """
    Delete a club from the database.

    This function performs the following actions:
    1. Sets club_id to NULL for any swimmers associated with the club
    2. Deletes the club

    Args:
    conn: Database connection object
    club_id: ID of the club to be deleted

    Returns:
    bool: True if the club was successfully deleted, False otherwise
    """
    try:
        cur = conn.cursor()

        # Set club_id to NULL for swimmers associated with the club
        cur.execute("UPDATE swimmers SET club_id = NULL WHERE club_id = %s", (club_id,))

        # Delete the club
        cur.execute("DELETE FROM clubs WHERE id = %s", (club_id,))

        affected_rows = cur.rowcount
        conn.commit()
        cur.close()

        if affected_rows > 0:
            logger.info(f"Club with ID {club_id} deleted successfully.")
            return True
        else:
            logger.warning(f"No club found with ID {club_id}.")
            return False

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f"Error deleting club: {error}")
        conn.rollback()
        return False

def update_club(conn, club_id, club_name=None, city=None, owner_id=None):
    """
    Update a club's information in the database.

    Args:
    conn: Database connection object
    club_id: ID of the club to be updated
    club_name: New name of the club (optional)
    city: New city of the club (optional)
    owner_id: New owner ID of the club (optional)

    Returns:
    bool: True if the club was successfully updated, False otherwise
    """
    try:
        cur = conn.cursor()
        update_fields = []
        update_values = []

        if club_name is not None:
            update_fields.append("name = %s")
            update_values.append(club_name)

        if city is not None:
            update_fields.append("city = %s")
            update_values.append(city)

        if owner_id is not None:
            update_fields.append("owner_id = %s")
            update_values.append(owner_id)

        if not update_fields:
            logger.warning("No fields to update for club.")
            return False

        sql = f"UPDATE clubs SET {', '.join(update_fields)} WHERE id = %s"
        update_values.append(club_id)

        cur.execute(sql, tuple(update_values))
        affected_rows = cur.rowcount
        conn.commit()
        cur.close()

        if affected_rows > 0:
            logger.info(f"Club with ID {club_id} updated successfully.")
            return True
        else:
            logger.warning(f"No club found with ID {club_id}.")
            return False

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f"Error updating club: {error}")
        conn.rollback()
        return False
