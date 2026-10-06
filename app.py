import streamlit as st
from modules.chatbot import get_response
from modules.summarizer import summarize_text
from modules.quiz import generate_quiz
from modules.planner import create_plan
if "progress" not in st.session_state:

    st.session_state.progress = 0
from modules.recommendation import get_recommendation

st.set_page_config(
    page_title="AI StudyMate",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 AI StudyMate")
st.subheader("Smart Learning Assistant")

st.write(
    "Welcome to AI StudyMate! "
    "Your personal AI-powered learning assistant."
)

st.sidebar.title("📚 Menu")

menu = st.sidebar.radio(
    "Select a Feature",
    [
        "🏠 Dashboard",
        "🤖 AI Chatbot",
        "📝 Summarizer",
        "❓ Quiz Generator",
        "📅 Study Planner",
        "📊 Progress",
        "💡 Recommendations"
    ]
)

if menu == "🏠 Dashboard":

    st.header("🎓 AI StudyMate Dashboard")

    st.write(
        "Your personalized smart learning assistant."
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📚 Subjects",
            "5"
        )

    with col2:
        st.metric(
            "📝 Quizzes",
            "12"
        )

    with col3:
        st.metric(
            "⏱ Study Hours",
            "24"
        )

    with col4:
        st.metric(
            "📊 Progress",
            "75%"
        )

    st.divider()

    st.subheader(
        "🚀 Available Features"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            "🤖 AI Chatbot\n\n"
            "Ask questions and get instant answers."
        )

        st.info(
            "📝 Notes Summarizer\n\n"
            "Convert lengthy notes into short summaries."
        )

    with col2:

        st.info(
            "❓ Quiz Generator\n\n"
            "Practice your knowledge with quizzes."
        )

        st.info(
            "📅 Study Planner\n\n"
            "Create personalized study schedules."
        )

elif menu == "🤖 AI Chatbot":

    st.header("🤖 AI Study Chatbot")

    question = st.text_input(
        "Ask your study question:"
    )

    if st.button("Ask AI"):

        if question:

            answer = get_response(question)
            st.write(answer)
        else:
            st.warning("Please enter a question.")

elif menu == "📝 Summarizer":

    st.header("📝 Notes Summarizer")

    uploaded_file = st.file_uploader(
        "Upload your notes",
        type=["txt"]
    )

    text = ""

    if uploaded_file:

        text = uploaded_file.read().decode(
            "utf-8"
        )

        st.text_area(
            "Uploaded Notes",
            text,
            height=200
        )

    else:

        text = st.text_area(
            "Or paste your notes here:",
            height=200
        )

    if st.button("Summarize"):

        if text:

            summary = summarize_text(text)

            st.subheader("📌 Summary")

            st.write(summary)

        else:

            st.warning(
                "Please upload or enter notes."
            )

elif menu == "❓ Quiz Generator":

    st.header("🤖 AI Quiz Generator")

    topic = st.text_input(
        "Enter any topic:",
        placeholder="Example: Machine Learning"
    )

    if st.button("✨ Generate 10 Questions"):

        if topic:

            with st.spinner(
                "🤖 Gemini is generating your quiz..."
            ):

                questions = generate_quiz(topic)

            if len(questions) >= 10:

                st.session_state.quiz_questions = questions[:10]
                st.session_state.quiz_topic = topic
                st.session_state.quiz_generated = True
                st.session_state.quiz_submitted = False

                st.success(
                    "✅ 10 questions generated successfully!"
                )

            else:

                st.error(
                    "Unable to generate 10 questions. "
                    "Please try again."
                )

        else:

            st.warning(
                "Please enter a topic first."
            )



    if st.session_state.get(
        "quiz_generated",
        False
    ):

        questions = st.session_state.quiz_questions

        st.subheader(
            f"📝 {st.session_state.quiz_topic} - AI Quiz"
        )

        st.write(
            "Answer all 10 questions and submit your quiz."
        )

        answers = []

        for i, q in enumerate(questions):

            st.markdown(
                f"### Question {i + 1}"
            )

            answer = st.radio(
                q["question"],
                q["options"],
                key=f"quiz_question_{i}"
            )

            answers.append(answer)


        if st.button("📊 Submit Quiz"):

            score = 0

            for i, q in enumerate(questions):

                if answers[i] == q["answer"]:

                    score += 1


            st.session_state.quiz_score = score
            st.session_state.quiz_submitted = True


        if st.session_state.get(
            "quiz_submitted",
            False
        ):

            score = st.session_state.quiz_score

            percentage = (score / 10) * 100

            st.divider()

            st.subheader("🎯 Quiz Result")

            st.success(
                f"Your Score: {score}/10"
            )

            st.write(
                f"Percentage: {percentage:.0f}%"
            )

            if score >= 8:

                st.balloons()

                st.success(
                    "Excellent! 🌟"
                )

            elif score >= 5:

                st.info(
                    "Good job! Keep practicing. 👍"
                )

            else:

                st.warning(
                    "You need more practice. 📚"
                )

elif menu == "📅 Study Planner":

    st.header("📅 Personalized Study Planner")

    subject = st.text_input(
        "Subject"
    )

    hours = st.number_input(
        "Study Hours",
        min_value=1,
        max_value=10,
        value=3
    )

    if st.button("Create Plan"):

        if subject:

            plan = create_plan(
                subject,
                hours
            )

            st.subheader("📚 Your Study Plan")

            for item in plan:

                st.write(
                    f"Hour {item['Hour']}: "
                    f"{item['Activity']} - "
                    f"{item['Subject']}"
                )

        else:

            st.warning(
                "Please enter a subject."
            )

elif menu == "📊 Progress":

    st.header("📊 Learning Progress")

    progress = st.slider(
        "Update your progress",
        0,
        100,
        st.session_state.progress
    )

    st.session_state.progress = progress

    st.progress(
        progress / 100
    )

    st.write(
        f"Overall Progress: {progress}%"
    )

elif menu == "💡 Recommendations":

    st.header("💡 Personalized Recommendations")

    score = st.slider(
        "Enter your quiz score",
        0,
        100,
        70
    )

    if st.button("Get Recommendation"):

        recommendation = get_recommendation(
            score
        )

        st.success(recommendation)