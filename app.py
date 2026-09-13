import streamlit as st
import sqlite3

from database import create_database


# Create the database
create_database()


# Page settings
st.set_page_config(
    page_title="Academic Survival Assistant",
    page_icon="🎓",
    layout="wide"
)


# Title
st.title("🎓 AI Academic Survival Assistant")

st.caption("Plan smarter. Study better. Stay ahead.")

st.divider()


# Add Academic Task
st.header("📋 Add Academic Task")


with st.form("task_form"):

    task_name = st.text_input(
        "Task name",
        placeholder="Example: DBMS Assignment"
    )

    subject = st.text_input(
        "Subject",
        placeholder="Example: Database Management Systems"
    )

    task_type = st.selectbox(
        "Task type",
        ["Assignment", "Exam", "Project", "Lab", "Other"]
    )

    deadline = st.date_input(
        "Deadline"
    )

    difficulty = st.slider(
        "Difficulty",
        min_value=1,
        max_value=10,
        value=5
    )

    estimated_hours = st.number_input(
        "Estimated hours",
        min_value=0.5,
        max_value=20.0,
        value=2.0,
        step=0.5
    )

    submitted = st.form_submit_button(
        "➕ Add Task"
    )


    # When Add Task is clicked
    if submitted:

        # Check required fields
        if task_name and subject:

            # Connect to database
            connection = sqlite3.connect("academic.db")

            cursor = connection.cursor()


            # Save task
            cursor.execute(
                """
                INSERT INTO tasks
                (
                    task_name,
                    subject,
                    task_type,
                    deadline,
                    difficulty,
                    estimated_hours
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    task_name,
                    subject,
                    task_type,
                    str(deadline),
                    difficulty,
                    estimated_hours
                )
            )


            # Save changes
            connection.commit()

            # Close database
            connection.close()


            # Success message
            st.success(
                f"✅ {task_name} saved successfully!"
            )

        else:

            st.warning(
                "⚠️ Please enter the task name and subject."
            )


   # -------------------------
# MY ACADEMIC TASKS
# -------------------------

st.divider()

st.header("📋 My Academic Tasks")


connection = sqlite3.connect("academic.db")

cursor = connection.cursor()

cursor.execute("""
    SELECT
        id,
        task_name,
        subject,
        task_type,
        deadline,
        difficulty,
        estimated_hours,
        completed
    FROM tasks
    ORDER BY deadline ASC
""")

tasks = cursor.fetchall()

connection.close()


# Display tasks

if tasks:

    for task in tasks:

        task_id = task[0]
        task_name = task[1]
        subject = task[2]
        task_type = task[3]
        deadline = task[4]
        difficulty = task[5]
        estimated_hours = task[6]
        completed = task[7]

        st.subheader(f"📌 {task_name}")

        st.write(f"**Subject:** {subject}")

        st.write(f"**Type:** {task_type}")

        st.write(f"**Deadline:** {deadline}")

        st.write(f"**Difficulty:** {difficulty}/10")

        st.write(f"**Estimated time:** {estimated_hours} hours")

        if completed:

            st.success("✅ Completed")

        else:

            st.warning("⏳ Pending")


        col1, col2 = st.columns(2)


        with col1:

            if not completed:

                if st.button(
                    "✅ Mark Complete",
                    key=f"complete_{task_id}"
                ):

                    connection = sqlite3.connect("academic.db")

                    cursor = connection.cursor()

                    cursor.execute(
                        "UPDATE tasks SET completed = 1 WHERE id = ?",
                        (task_id,)
                    )

                    connection.commit()

                    connection.close()

                    st.rerun()


        with col2:

            if st.button(
                "🗑️ Delete",
                key=f"delete_{task_id}"
            ):

                connection = sqlite3.connect("academic.db")

                cursor = connection.cursor()

                cursor.execute(
                    "DELETE FROM tasks WHERE id = ?",
                    (task_id,)
                )

                connection.commit()

                connection.close()

                st.rerun()


        st.divider()


else:

    st.info("No academic tasks added yet.")
    