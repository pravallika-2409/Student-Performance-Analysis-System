
import pandas as pd
from config.database import get_connection


def get_students():
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT student_id, roll_no, name, section "
            "FROM students ORDER BY roll_no"
        )
        rows = cur.fetchall()
        columns = [col[0] for col in cur.description]
        return pd.DataFrame(rows, columns=columns)
    finally:
        conn.close()


def add_student(roll_no, name, section):
    if not roll_no or not name or not section:
        raise ValueError("Roll number, name, and section are required.")
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO students (roll_no, name, section) VALUES (%s,%s,%s)",
            (roll_no, name, section)
        )
        conn.commit()
    finally:
        conn.close()


def update_student(student_id, roll_no, name, section):
    if not roll_no or not name or not section:
        raise ValueError("All student fields are required.")
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE students SET roll_no=%s, name=%s, section=%s WHERE student_id=%s",
            (roll_no, name, section, student_id)
        )
        conn.commit()
    finally:
        conn.close()


def delete_student(student_id):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM students WHERE student_id=%s",
            (student_id,)
        )
        conn.commit()
    finally:
        conn.close()
