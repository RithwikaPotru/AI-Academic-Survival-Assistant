import streamlit as st
import sqlite3
import textwrap
from datetime import date
from openai import OpenAI
from database import create_database

# Page settings
st.set_page_config(
    page_title="Academic Survival Assistant",
    page_icon="🎓",
    layout="wide"
)
client = OpenAI()

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(59,130,246,0.18), transparent 30%),
        radial-gradient(circle at 90% 20%, rgba(139,92,246,0.16), transparent 30%),
        linear-gradient(135deg, #07111f 0%, #0b172a 50%, #111827 100%);
    color: #f8fafc;
}

/* Main content */
.block-container {
    max-width: 1200px;
    padding-top: 3rem;
    padding-bottom: 4rem;
}

/* Main headings */
h1 {
    font-size: 2.8rem !important;
    font-weight: 800 !important;
    letter-spacing: -1px;
    color: #f8fafc !important;
}

h2 {
    font-size: 2rem !important;
    font-weight: 750 !important;
    color: #f1f5f9 !important;
}

h3 {
    color: #e2e8f0 !important;
}

/* Normal text */
p, label, .stMarkdown {
    color: #cbd5e1;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: rgba(20, 35, 58, 0.85) !important;
    border: 1px solid rgba(96, 165, 250, 0.18) !important;
    border-radius: 18px !important;
    padding: 24px !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.30) !important;
}

[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
}

[data-testid="stMetricValue"] {
    color: #f8fafc !important;
    font-weight: 700 !important;
}

/* Dropdown */
div[data-baseweb="select"] > div {
    background-color: #0f1e32 !important;
    color: #f8fafc !important;
    border: 1px solid rgba(148, 163, 184, 0.20) !important;
    border-radius: 12px !important;
}

div[data-baseweb="select"] span {
    color: #f8fafc !important;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    border-color: rgba(96,165,250,0.4);
    box-shadow: 0 16px 40px rgba(0,0,0,0.35);
}

[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
}

[data-testid="stMetricValue"] {
    color: #f8fafc !important;
    font-weight: 700;
}

/* Input fields */
.stTextInput input,
.stNumberInput input,
.stDateInput input,
.stSelectbox div[data-baseweb="select"] {
    background: rg.2) !important;
    border-radius: 12px !important;
}
ba(15, 30, 50, 0.8) !important;
    color: #f8fafc !important;
    border: 1px solid rgba(148,163,184,0
/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.75rem 1.6rem;
    font-weight: 700;
    transition: all 0.25s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(37,99,235,0.35);
}

/* Task cards / containers */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(15, 30, 50, 0.65);
    border: 1px solid rgba(148,163,184,0.14);
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.20);
}

/* Alerts */
div[data-testid="stAlert"] {
    border-radius: 14px;
}

/* Divider */
hr {
    border-color: rgba(148,163,184,0.12) !important;
    margin: 2rem 0 !important;
}

/* Slider */
.stSlider {
    padding-top: 10px;
}

/* Hide Streamlit branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

st.markdown("""

""", unsafe_allow_html=True)

/* Dashboard metric cards */
[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 18px;
    padding: 20px;
    min-height: 120px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.18);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.28);
}

[data-testid="stMetricLabel"] {
    font-size: 16px;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    font-size: 32px;
    font-weight: 700;
}

/* FINAL AI CHAT INPUT TEXT FIX */

div[data-testid="stChatInput"] textarea,
div[data-baseweb="textarea"] textarea {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    background-color: #ffffff !important;
    caret-color: #000000 !important;
}

div[data-testid="stChatInput"] textarea:focus,
div[data-baseweb="textarea"] textarea:focus {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    background-color: #ffffff !important;
    caret-color: #000000 !important;
}

div[data-testid="stChatInput"] textarea::placeholder,
div[data-baseweb="textarea"] textarea::placeholder {
    color: #555555 !important;
    -webkit-text-fill-color: #555555 !important;
    opacity: 1 !important;
}

</style>
""", unsafe_allow_html=True)


# CUSTOM UI STYLING


st.markdown("""
<style>

.main {
    background-color: #f7f9fc;
}

h1 {
    color: #1f2937;
    font-size: 42px !important;
    font-weight: 700;
}

h2 {
    color: #374151;
}

h3 {
    color: #4b5563;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

/* Buttons */
.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    padding: 8px 20px;
}

/* Input boxes */
.stTextInput input,
.stNumberInput input,
.stDateInput input {
    border-radius: 10px;
}

/* Sections */
hr {
    margin-top: 30px;
    margin-bottom: 30px;
}

/* Academic Task Form Labels */
[data-testid="stWidgetLabel"] p {
    color: #f1f5f9 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    letter-spacing: 0.2px !important;
}

.stTextInput label,
.stSelectbox label,
.stDateInput label,
.stSlider label,
.stNumberInput label {
    color: #f1f5f9 !important;
    font-weight: 600 !important;
}


</style>
""", unsafe_allow_html=True)



# Title
create_database()


# DASHBOARD HEADER


st.title("🎓 AI Academic Survival Assistant")
st.caption("Plan smarter. Study better. Stay ahead.")

# Get task statistics
connection = sqlite3.connect("academic.db")
cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM tasks")
total_tasks = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM tasks WHERE completed = 0")
pending_tasks_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM tasks WHERE completed = 1")
completed_tasks_count = cursor.fetchone()[0]

cursor.execute("""
    SELECT COUNT(*)
    FROM tasks
    WHERE completed = 0
    AND deadline <= date('now', '+3 days')
""")
due_soon_count = cursor.fetchone()[0]

connection.close()

# Dashboard cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📚 Total Tasks",
        total_tasks
    )

with col2:
    st.metric(
        "⏳ Pending",
        pending_tasks_count
    )

with col3:
    st.metric(
        "✅ Completed",
        completed_tasks_count
    )

with col4:
    st.metric(
        "🚨 Due Soon",
        due_soon_count
    )

st.divider()

# Overall progress
if total_tasks > 0:
    progress = (completed_tasks_count / total_tasks) * 100
else:
    progress = 0

st.write("### 🎯 Overall Progress")

st.progress(progress / 100)

st.caption(
    f"You have completed {progress:.0f}% of your academic tasks."
)

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

st.divider()

# -----------------------------
# SMART TASK PRIORITY
# -----------------------------

st.header("🔥 Smart Task Priority")

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
    WHERE completed = 0
    ORDER BY deadline ASC
""")

pending_tasks = cursor.fetchall()
connection.close()

if pending_tasks:

    from datetime import date, datetime

    priority_tasks = []

    for task in pending_tasks:

        task_id = task[0]
        task_name = task[1]
        subject = task[2]
        task_type = task[3]
        deadline = task[4]
        difficulty = task[5]
        estimated_hours = task[6]

        try:
            deadline_date = datetime.strptime(
                deadline, "%Y-%m-%d"
            ).date()

            days_left = (deadline_date - date.today()).days

        except:
            days_left = 7

        # Deadline score
        if days_left <= 0:
            deadline_score = 10
        elif days_left <= 2:
            deadline_score = 9
        elif days_left <= 5:
            deadline_score = 7
        elif days_left <= 7:
            deadline_score = 5
        else:
            deadline_score = 3

        # Difficulty score
        difficulty_score = difficulty

        # Estimated time score
        time_score = min(estimated_hours / 2, 10)

        # Final priority score
        priority_score = (
            deadline_score * 0.5
            + difficulty_score * 0.3
            + time_score * 0.2
        )

        priority_tasks.append(
            (
                priority_score,
                task_name,
                subject,
                deadline,
                difficulty,
                estimated_hours,
                days_left
            )
        )

    # Highest priority first
    priority_tasks.sort(reverse=True)

    top_task = priority_tasks[0]

    score = top_task[0]
    name = top_task[1]
    subject = top_task[2]
    deadline = top_task[3]
    difficulty = top_task[4]
    hours = top_task[5]
    days_left = top_task[6]

    st.subheader(f"🚨 Start With: {name}")

    st.write(f"**Subject:** {subject}")
    st.write(f"**Deadline:** {deadline}")
    st.write(f"**Difficulty:** {difficulty}/10")
    st.write(f"**Estimated time:** {hours} hours")

    if days_left < 0:
        st.error("⚠️ This task is overdue!")

    elif days_left == 0:
        st.error("🚨 Deadline is today!")

    elif days_left == 1:
        st.warning("🔥 Deadline is tomorrow!")

    elif days_left <= 3:
        st.warning(f"⏰ Only {days_left} days left!")

    else:
        st.info(f"📅 {days_left} days remaining.")

    st.metric(
        "Priority Score",
        f"{score:.1f}/10"
    )

else:

    st.success("🎉 No pending tasks! You're all caught up.")

# -----------------------------
# MY ACADEMIC TASKS
# -----------------------------

st.divider()

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

        with st.container(border=True):

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
# ==============================
# 🤖 AI ACADEMIC ASSISTANT
# ==============================

st.divider()

st.header("🤖 AI Academic Assistant")
st.write(
    "Ask me anything about your academic tasks, deadlines, priorities, or study decisions."
)

# Quick AI Questions
st.markdown("### 💡 Try asking")

q1, q2, q3, q4 = st.columns(4)

with q1:
    if st.button("🎯 What should I do first?"):
        st.session_state.ai_quick_question = (
            "What should I complete first based on my current academic tasks?"
        )

with q2:
    if st.button("⏰ What is urgent?"):
        st.session_state.ai_quick_question = (
            "Which of my current tasks are the most urgent and why?"
        )

with q3:
    if st.button("📚 Help me plan"):
        st.session_state.ai_quick_question = (
            "Help me create a realistic plan for completing my pending academic tasks."
        )

with q4:
    if st.button("⚡ I have 2 hours"):
        st.session_state.ai_quick_question = (
            "I only have 2 hours today. What should I work on and how should I use those 2 hours?"
        )


# Get current tasks from database
connection = sqlite3.connect("academic.db")
cursor = connection.cursor()

cursor.execute("""
    SELECT task_name, subject, task_type, deadline,
           difficulty, estimated_hours, completed
    FROM tasks
    ORDER BY deadline ASC
""")

tasks = cursor.fetchall()
connection.close()

# Convert tasks into readable AI context
if tasks:
    task_context = "\n".join(
        [
            f"""
Task: {task[0]}
Subject: {task[1]}
Type: {task[2]}
Deadline: {task[3]}
Difficulty: {task[4]}/10
Estimated Hours: {task[5]}
Status: {"Completed" if task[6] else "Pending"}
"""
            for task in tasks
        ]
    )
else:
    task_context = "No academic tasks have been added yet."

# Chat history
if "ai_messages" not in st.session_state:
    st.session_state.ai_messages = []

# Display previous messages
for message in st.session_state.ai_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User question
user_question = st.chat_input(
    "Ask your academic assistant..."
)

if "ai_quick_question" in st.session_state:
    user_question = st.session_state.ai_quick_question
    del st.session_state.ai_quick_question


if user_question:

    # Show user message
    st.session_state.ai_messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    with st.chat_message("user"):
        st.markdown(user_question)

    # AI instructions
    instructions = """
You are an intelligent Academic Survival Assistant.

Your job is to help students manage their academic workload.

You have access to the student's actual academic tasks provided below.

Give practical, personalized and clear advice.

You can help with:
- deciding which task to do first
- managing deadlines
- estimating workload
- prioritizing difficult tasks
- creating short study plans
- preparing for exams
- balancing multiple subjects
- deciding what to complete when time is limited

Important rules:
1. Use the student's actual task information whenever relevant.
2. Never invent tasks, deadlines or progress.
3. If information is missing, clearly say so.
4. Keep recommendations realistic.
5. Consider deadline, difficulty and estimated hours.
6. The student may have ANY subject, so do not assume a specific subject.
7. Explain your reasoning briefly.
8. Give actionable next steps.
"""

    today = date.today().strftime("%B %d, %Y")

    prompt = f"""
    Today's date is: {today}

    Student's current academic tasks:

    {task_context}

    Student's question:

    {user_question}
    """

    try:
        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                response = client.responses.create(
                    model="gpt-5.6-luna",
                    instructions=instructions,
                    input=prompt
                )

                answer = response.output_text

            st.markdown(answer)

        st.session_state.ai_messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    except Exception as e:
        st.error(
            "I couldn't connect to the AI service. "
            "Please check your API key and internet connection."
        )