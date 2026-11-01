import pandas as pd
import numpy as np
from config.database import get_connection

def _read(query, params=None):
    conn = get_connection()
    try:
        return pd.read_sql(query, conn, params=params)
    finally:
        conn.close()

def _marks_frame():
    return _read("""
        SELECT s.student_id, s.roll_no, s.name, s.section,
               sub.subject_name, sub.max_marks, sub.pass_marks,
               m.marks_obtained, m.assessment
        FROM marks m
        JOIN students s ON s.student_id=m.student_id
        JOIN subjects sub ON sub.subject_id=m.subject_id
    """)

def student_summary():
    df = _marks_frame()
    if df.empty:
        return pd.DataFrame(columns=["roll_no","name","section","total_marks","maximum_marks","average_marks","percentage","grade","result"])
    # Each saved assessment is one record. All recorded assessments contribute to the student's aggregate.
    result = df.groupby(["student_id","roll_no","name","section"], as_index=False).agg(
        total_marks=("marks_obtained","sum"),
        maximum_marks=("max_marks","sum"),
        average_marks=("marks_obtained","mean"),
        assessment_count=("marks_obtained","count")
    )
    result["percentage"] = np.where(result["maximum_marks"] > 0,
                                    result["total_marks"] / result["maximum_marks"] * 100, 0)
    result["grade"] = result["percentage"].apply(_grade)
    result["result"] = result["percentage"].apply(lambda x: "Pass" if x >= 40 else "Fail")
    return result[["roll_no","name","section","total_marks","maximum_marks","average_marks","percentage","grade","result"]].round(2)

def _grade(p):
    if p >= 90: return "A+"
    if p >= 80: return "A"
    if p >= 70: return "B"
    if p >= 60: return "C"
    if p >= 50: return "D"
    if p >= 40: return "E"
    return "F"

def subject_summary():
    df = _marks_frame()
    if df.empty:
        return pd.DataFrame(columns=["subject_name","average_marks","median_marks","minimum_marks","maximum_obtained","pass_percentage","record_count"])
    grouped = df.groupby("subject_name").agg(
        average_marks=("marks_obtained","mean"),
        median_marks=("marks_obtained","median"),
        minimum_marks=("marks_obtained","min"),
        maximum_obtained=("marks_obtained","max"),
        record_count=("marks_obtained","count")
    ).reset_index()
    pass_rates = df.assign(passed=df["marks_obtained"] >= df["pass_marks"]).groupby("subject_name")["passed"].mean() * 100
    grouped["pass_percentage"] = grouped["subject_name"].map(pass_rates)
    return grouped.round(2)

def section_summary():
    summary = student_summary()
    if summary.empty:
        return pd.DataFrame(columns=["section","students","average_percentage","pass_percentage"])
    return summary.groupby("section").agg(
        students=("roll_no","count"),
        average_percentage=("percentage","mean"),
        pass_percentage=("result",lambda x: (x == "Pass").mean()*100)
    ).reset_index().round(2)

def get_low_performers(threshold=40):
    summary = student_summary()
    if summary.empty:
        return summary
    return summary[summary["percentage"] < threshold].reset_index(drop=True)
