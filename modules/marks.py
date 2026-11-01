import pandas as pd
from config.database import get_connection

def get_marks():
    query = """
    SELECT m.mark_id, s.roll_no, s.name, s.section, sub.subject_name,
           m.assessment, m.marks_obtained, sub.max_marks, sub.pass_marks
    FROM marks m
    JOIN students s ON m.student_id=s.student_id
    JOIN subjects sub ON m.subject_id=sub.subject_id
    ORDER BY s.roll_no, sub.subject_name, m.assessment
    """
    conn = get_connection()
    try:
        return pd.read_sql(query, conn)
    finally:
        conn.close()

def add_mark(student_id, subject_id, assessment, marks_obtained):
    if not assessment:
        raise ValueError("Assessment name is required.")
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT max_marks FROM subjects WHERE subject_id=%s", (subject_id,))
        row = cur.fetchone()
        if row is None:
            raise ValueError("Subject does not exist.")
        if marks_obtained < 0 or marks_obtained > float(row[0]):
            raise ValueError(f"Marks must be between 0 and {row[0]}.")
        cur.execute(
            "INSERT INTO marks (student_id, subject_id, assessment, marks_obtained) VALUES (%s,%s,%s,%s)",
            (student_id, subject_id, assessment, marks_obtained)
        )
        conn.commit()
    finally:
        conn.close()

def update_mark(mark_id, marks_obtained):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT sub.max_marks FROM marks m
            JOIN subjects sub ON m.subject_id=sub.subject_id
            WHERE m.mark_id=%s
        """, (mark_id,))
        row = cur.fetchone()
        if row is None:
            raise ValueError("Mark record not found.")
        if marks_obtained < 0 or marks_obtained > float(row[0]):
            raise ValueError(f"Marks must be between 0 and {row[0]}.")
        cur.execute("UPDATE marks SET marks_obtained=%s WHERE mark_id=%s",
                    (marks_obtained, mark_id))
        conn.commit()
    finally:
        conn.close()

def delete_mark(mark_id):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM marks WHERE mark_id=%s", (mark_id,))
        conn.commit()
    finally:
        conn.close()
