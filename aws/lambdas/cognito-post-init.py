import os
import psycopg2


def lambda_handler(event, context):
    user = event["request"]["userAttributes"]
    conn = None

    try:
        conn = psycopg2.connect(os.getenv("CONNECTION_URL"))
        cur = conn.cursor()
        sql = "INSERT INTO users (email, display_name, handle, cognito_user_id) VALUES(%s, %s, %s, %s)"
        cur.execute(
            sql,
            (user["email"], user["name"], user["preferred_username"], user["sub"]),
        )
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            cur.close()
            conn.close()
            print("Database connection closed.")

    return event
