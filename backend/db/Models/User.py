import psycopg2
import logging

logger = logging.getLogger(__name__)    

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

def delete_user(conn, user_id):
    try:
        cur = conn.cursor()

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
    
def update_user(conn, user_id, email=None, password_hash=None):
    """
    Update a user's information in the database.

    Args:
    conn: Database connection object
    user_id: ID of the user to be updated
    email: New email address (optional)
    password_hash: New password hash (optional)

    Returns:
    bool: True if the user was successfully updated, False otherwise
    """
    try:
        cur = conn.cursor()
        update_fields = []
        update_values = []

        if email is not None:
            update_fields.append("email = %s")
            update_values.append(email)

        if password_hash is not None:
            update_fields.append("password_hash = %s")
            update_values.append(password_hash)

        if not update_fields:
            logger.warning("No fields to update for user.")
            return False

        sql = f"UPDATE users SET {', '.join(update_fields)} WHERE id = %s"
        update_values.append(user_id)

        cur.execute(sql, tuple(update_values))
        affected_rows = cur.rowcount
        conn.commit()
        cur.close()

        if affected_rows > 0:
            logger.info(f"User with ID {user_id} updated successfully.")
            return True
        else:
            logger.warning(f"No user found with ID {user_id}.")
            return False

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f"Error updating user: {error}")
        conn.rollback()
        return False
