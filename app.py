import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from config.database import get_connection
from modules.students import get_students, add_student, update_student, delete_student
from modules.subjects import get_subjects, add_subject, delete_subject
from modules.marks import get_marks, add_mark, update_mark, delete_mark
from modules.analytics import student_summary, subject_summary, section_summary, get_low_performers

st.set_page_config(page_title="Student Performance Analysis", page_icon="🎓", layout="wide")

st.title("🎓 Student Performance Analysis System")
st.caption("Manage academic records and understand student performance.")

def db_check():
    try:
        conn = get_connection()
        conn.close()
        return True
    except Exception as exc:
        st.error(f"Cannot connect to MySQL: {exc}")
        st.info("Check that MySQL is running, the database has been created, and your .env settings are correct.")
        return False

if not db_check():
    st.stop()

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Students", "Subjects", "Marks", "Performance Reports"]
)

if page == "Dashboard":
    students = get_students()
    subjects = get_subjects()
    marks = get_marks()
    summary = student_summary()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Students", len(students))
    c2.metric("Subjects", len(subjects))
    c3.metric("Mark records", len(marks))
    c4.metric("Students analysed", len(summary))

    st.subheader("Subject-wise average marks")
    subject_data = subject_summary()
    if not subject_data.empty:
        fig, ax = plt.subplots()
        ax.bar(subject_data["subject_name"], subject_data["average_marks"])
        ax.set_ylabel("Average marks")
        ax.set_xlabel("Subject")
        ax.set_ylim(bottom=0)
        plt.xticks(rotation=25, ha="right")
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("Add marks to see the subject-wise chart.")

    st.subheader("Recent student records")
    st.dataframe(students, use_container_width=True, hide_index=True)

elif page == "Students":
    st.header("Student records")
    with st.expander("➕ Add a student", expanded=True):
        with st.form("add_student_form"):
            roll = st.text_input("Roll number")
            name = st.text_input("Student name")
            section = st.text_input("Section", value="A")
            submitted = st.form_submit_button("Add student")
            if submitted:
                try:
                    add_student(roll.strip(), name.strip(), section.strip())
                    st.success("Student added.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Could not add student: {exc}")

    students = get_students()
    st.dataframe(students, use_container_width=True, hide_index=True)
    if not students.empty:
        st.subheader("Update or delete a student")
        chosen = st.selectbox("Select student", students["student_id"].tolist(),
                              format_func=lambda x: f'{x} - {students.loc[students.student_id == x, "name"].iloc[0]}')
        current = students[students.student_id == chosen].iloc[0]
        with st.form("edit_student_form"):
            new_roll = st.text_input("Roll number", value=str(current["roll_no"]))
            new_name = st.text_input("Name", value=str(current["name"]))
            new_section = st.text_input("Section", value=str(current["section"]))
            a, b = st.columns(2)
            update = a.form_submit_button("Save changes")
            remove = b.form_submit_button("Delete student")
            if update:
                try:
                    update_student(chosen, new_roll.strip(), new_name.strip(), new_section.strip())
                    st.success("Student updated.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Update failed: {exc}")
            if remove:
                try:
                    delete_student(chosen)
                    st.success("Student and related marks deleted.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Delete failed: {exc}")

elif page == "Subjects":
    st.header("Subject management")
    with st.form("add_subject_form"):
        subject_name = st.text_input("Subject name")
        max_marks = st.number_input("Maximum marks", min_value=1, value=100, step=1)
        pass_marks = st.number_input("Pass marks", min_value=0, value=40, step=1)
        submit = st.form_submit_button("Add subject")
        if submit:
            try:
                if pass_marks > max_marks:
                    st.error("Pass marks cannot exceed maximum marks.")
                else:
                    add_subject(subject_name.strip(), int(max_marks), int(pass_marks))
                    st.success("Subject added.")
                    st.rerun()
            except Exception as exc:
                st.error(f"Could not add subject: {exc}")

    subjects = get_subjects()
    st.dataframe(subjects, use_container_width=True, hide_index=True)
    if not subjects.empty:
        subject_id = st.selectbox(
            "Select a subject to delete", subjects["subject_id"].tolist(),
            format_func=lambda x: f'{x} - {subjects.loc[subjects.subject_id == x, "subject_name"].iloc[0]}'
        )
        if st.button("Delete selected subject"):
            try:
                delete_subject(subject_id)
                st.success("Subject deleted.")
                st.rerun()
            except Exception as exc:
                st.error(f"Delete failed: {exc}")

elif page == "Marks":
    st.header("Assessment marks")
    students = get_students()
    subjects = get_subjects()
    if students.empty or subjects.empty:
        st.warning("Add at least one student and one subject before entering marks.")
    else:
        with st.form("add_mark_form"):
            student_id = st.selectbox(
                "Student", students["student_id"].tolist(),
                format_func=lambda x: f'{students.loc[students.student_id == x, "roll_no"].iloc[0]} - {students.loc[students.student_id == x, "name"].iloc[0]}'
            )
            subject_id = st.selectbox(
                "Subject", subjects["subject_id"].tolist(),
                format_func=lambda x: subjects.loc[subjects.subject_id == x, "subject_name"].iloc[0]
            )
            assessment = st.text_input("Assessment name", value="Internal 1")
            max_for_subject = int(subjects.loc[subjects.subject_id == subject_id, "max_marks"].iloc[0])
            obtained = st.number_input("Marks obtained", min_value=0.0, max_value=float(max_for_subject), value=0.0, step=1.0)
            submit = st.form_submit_button("Save marks")
            if submit:
                try:
                    add_mark(student_id, subject_id, assessment.strip(), obtained)
                    st.success("Marks saved.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Could not save marks: {exc}")

    marks = get_marks()
    st.subheader("Saved marks")
    st.dataframe(marks, use_container_width=True, hide_index=True)
    if not marks.empty:
        mark_id = st.selectbox("Select mark record", marks["mark_id"].tolist(),
                               format_func=lambda x: f"Record {x}")
        record = marks[marks.mark_id == mark_id].iloc[0]
        max_value = float(record["max_marks"])
        with st.form("edit_mark_form"):
            revised = st.number_input("Corrected marks", min_value=0.0, max_value=max_value,
                                      value=float(record["marks_obtained"]), step=1.0)
            col1, col2 = st.columns(2)
            update = col1.form_submit_button("Update marks")
            remove = col2.form_submit_button("Delete mark record")
            if update:
                try:
                    update_mark(mark_id, revised)
                    st.success("Marks updated.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Update failed: {exc}")
            if remove:
                delete_mark(mark_id)
                st.success("Mark record deleted.")
                st.rerun()

elif page == "Performance Reports":
    st.header("Performance reports")
    threshold = st.slider("Low-performance threshold (%)", 0, 100, 40)
    summary = student_summary()
    if summary.empty:
        st.info("No marks available yet. Add assessment marks to generate reports.")
    else:
        st.subheader("Student performance report")
        st.dataframe(summary, use_container_width=True, hide_index=True)

        st.subheader("Top-performing students")
        st.dataframe(summary.sort_values("percentage", ascending=False).head(10),
                     use_container_width=True, hide_index=True)

        st.subheader(f"Students below {threshold}%")
        low = get_low_performers(threshold)
        st.dataframe(low, use_container_width=True, hide_index=True)

        st.subheader("Subject-wise summary")
        subjects_report = subject_summary()
        st.dataframe(subjects_report, use_container_width=True, hide_index=True)
        if not subjects_report.empty:
            fig, ax = plt.subplots()
            ax.bar(subjects_report["subject_name"], subjects_report["pass_percentage"])
            ax.set_ylabel("Pass percentage")
            ax.set_ylim(0, 100)
            plt.xticks(rotation=25, ha="right")
            st.pyplot(fig)
            plt.close(fig)

        st.subheader("Section-wise summary")
        st.dataframe(section_summary(), use_container_width=True, hide_index=True)

        csv = summary.to_csv(index=False).encode("utf-8")
        st.download_button("Download student report (CSV)", csv,
                           "student_performance_report.csv", "text/csv")

st.sidebar.divider()
st.sidebar.caption("Student Performance Analysis System")
