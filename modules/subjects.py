import pandas as pd
from config.database import get_connection

def get_subjects():
    conn = get_connection()
    try:
        return pd.read_sql("SELECT subject_id, subject_name, max_marks, pass_marks FROM subjects ORDER BY subject_name", conn)
    finally:
        conn.close()

def add_subject(name, max_marks, pass_marks):
    if not name:
        raise ValueError("Subject name is required.")
    if max_marks <= 0 or pass_marks < 0 or pass_marks > max_marks:
        raise ValueError("Enter valid maximum and pass marks.")
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO subjects (subject_name, max_marks, pass_marks) VALUES (%s,%s,%s)",
                    (name, max_marks, pass_marks))
        conn.commit()
    finally:
        conn.close()

def delete_subject(subject_id):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM subjects WHERE subject_id=%s", (subject_id,))
        conn.commit()
    finally:
        conn.close()
