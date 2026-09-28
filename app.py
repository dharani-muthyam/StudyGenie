import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

# ============================================================
# SETUP
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    client = genai.Client(api_key=api_key)
else:
    client = None

st.set_page_config(
    page_title="StudyGenie",
    page_icon="🎓",
    layout="wide"
)

# ============================================================
# CUSTOM CSS
# ============================================================

css = "\n".join([
    "<style>",
    ".stApp { background-color: #f6f8fc; }",
    "#MainMenu { visibility: hidden; }",
    "footer { visibility: hidden; }",
    "header { visibility: hidden; }",
    ".block-container { max-width: 1100px; padding-top: 2rem; padding-bottom: 3rem; }",

    ".logo {",
    "font-size: 30px;",
    "font-weight: 800;",
    "color: #3158d5;",
    "margin-bottom: 25px;",
    "}",

    ".hero {",
    "background: white;",
    "border-radius: 25px;",
    "padding: 45px;",
    "border: 1px solid #e5e8f0;",
    "box-shadow: 0 12px 35px rgba(30,50,90,0.08);",
    "margin-bottom: 25px;",
    "}",

    ".small-label {",
    "font-size: 13px;",
    "font-weight: 700;",
    "letter-spacing: 1.5px;",
    "color: #536ee0;",
    "margin-bottom: 12px;",
    "}",

    ".hero-title {",
    "font-size: 45px;",
    "font-weight: 800;",
    "line-height: 1.15;",
    "color: #172033;",
    "margin-bottom: 15px;",
    "}",

    ".hero-highlight { color: #536ee0; }",

    ".hero-text {",
    "font-size: 17px;",
    "line-height: 1.7;",
    "color: #697286;",
    "max-width: 700px;",
    "}",

    ".welcome {",
    "background: linear-gradient(135deg, #edf2ff, #f7f4ff);",
    "border: 1px solid #dfe5ff;",
    "border-radius: 22px;",
    "padding: 28px;",
    "margin-bottom: 28px;",
    "}",

    ".welcome-title {",
    "font-size: 30px;",
    "font-weight: 800;",
    "color: #20283a;",
    "}",

    ".welcome-text {",
    "font-size: 16px;",
    "color: #6c7486;",
    "margin-top: 5px;",
    "}",

    ".feature {",
    "background: white;",
    "border: 1px solid #e4e7ef;",
    "border-radius: 18px;",
    "padding: 22px;",
    "min-height: 135px;",
    "box-shadow: 0 7px 22px rgba(30,50,90,0.05);",
    "}",

    ".feature-icon {",
    "font-size: 28px;",
    "margin-bottom: 8px;",
    "}",

    ".feature-title {",
    "font-size: 17px;",
    "font-weight: 750;",
    "color: #20283a;",
    "}",

    ".feature-text {",
    "font-size: 13px;",
    "line-height: 1.5;",
    "color: #737c8f;",
    "margin-top: 5px;",
    "}",

    ".result {",
    "background: white;",
    "border: 1px solid #e2e6ef;",
    "border-radius: 20px;",
    "padding: 28px;",
    "box-shadow: 0 8px 25px rgba(30,50,90,0.06);",
    "margin-top: 20px;",
    "}",

    ".footer {",
    "text-align: center;",
    "color: #9aa2b2;",
    "font-size: 13px;",
    "margin-top: 45px;",
    "}",

    ".stButton > button {",
    "border-radius: 11px;",
    "font-weight: 700;",
    "min-height: 44px;",
    "}",

    ".stTextInput input, .stTextArea textarea {",
    "border-radius: 11px;",
    "}",

    "</style>"
])

st.markdown(css, unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "result" not in st.session_state:
    st.session_state.result = ""

# ============================================================
# FUNCTIONS
# ============================================================

def login_user(name):
    st.session_state.logged_in = True
    st.session_state.user_name = name


def logout_user():
    st.session_state.logged_in = False
    st.session_state.user_name = ""
    st.session_state.result = ""

# ============================================================
# LOGO
# ============================================================

st.markdown(
    '<div class="logo">🎓 StudyGenie</div>',
    unsafe_allow_html=True
)

# ============================================================
# LOGIN / SIGNUP PAGE
# ============================================================

if not st.session_state.logged_in:

    hero_html = "\n".join([
        '<div class="hero">',
        '<div class="small-label">AI-POWERED LEARNING</div>',
        '<div class="hero-title">Learn smarter.<br><span class="hero-highlight">Study better.</span></div>',
        '<div class="hero-text">',
        'StudyGenie is your AI-powered study companion. ',
        'Understand difficult topics, summarize your notes, ',
        'generate quizzes, and ask questions in simple language.',
        '</div>',
        '</div>'
    ])

    st.markdown(hero_html, unsafe_allow_html=True)

    login_tab, signup_tab = st.tabs([
        "🔐 Log In",
        "✨ Create Account"
    ])

    # --------------------------------------------------------
    # LOGIN
    # --------------------------------------------------------

    with login_tab:

        st.subheader("Welcome back 👋")

        login_email = st.text_input(
            "Email",
            placeholder="Enter your email",
            key="login_email"
        )

        login_password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )

        if st.button(
            "Log In →",
            use_container_width=True,
            key="login_btn"
        ):

            if login_email.strip() and login_password.strip():

                username = login_email.split("@")[0]
                username = username.replace(".", " ")
                username = username.title()

                login_user(username)
                st.rerun()

            else:
                st.warning("Please enter your email and password.")

    # --------------------------------------------------------
    # SIGN UP
    # --------------------------------------------------------

    with signup_tab:

        st.subheader("Create your StudyGenie account")

        signup_name = st.text_input(
            "Full Name",
            placeholder="Enter your name",
            key="signup_name"
        )

        signup_email = st.text_input(
            "Email",
            placeholder="Enter your email",
            key="signup_email"
        )

        signup_password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password",
            key="signup_password"
        )

        if st.button(
            "Create Account →",
            use_container_width=True,
            key="signup_btn"
        ):

            if (
                signup_name.strip()
                and signup_email.strip()
                and signup_password.strip()
            ):

                login_user(signup_name.strip())
                st.rerun()

            else:
                st.warning("Please fill in all fields.")

# ============================================================
# DASHBOARD
# ============================================================

else:

    top_left, top_right = st.columns([5, 1])

    with top_left:
        st.caption("STUDENT DASHBOARD")

    with top_right:
        if st.button(
            "Logout",
            use_container_width=True,
            key="logout_btn"
        ):
            logout_user()
            st.rerun()

    # --------------------------------------------------------
    # WELCOME
    # --------------------------------------------------------

    welcome_html = "\n".join([
        '<div class="welcome">',
        f'<div class="welcome-title">Hello, {st.session_state.user_name}! 👋</div>',
        '<div class="welcome-text">',
        'What would you like to learn today? Let StudyGenie help you.',
        '</div>',
        '</div>'
    ])

    st.markdown(welcome_html, unsafe_allow_html=True)

    # --------------------------------------------------------
    # FEATURE CARDS
    # --------------------------------------------------------

    st.markdown(
        '<div class="small-label">STUDY TOOLS</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        feature_html = "\n".join([
            '<div class="feature">',
            '<div class="feature-icon">💡</div>',
            '<div class="feature-title">Explain a Topic</div>',
            '<div class="feature-text">',
            'Understand difficult concepts with simple explanations and examples.',
            '</div>',
            '</div>'
        ])

        st.markdown(feature_html, unsafe_allow_html=True)

    with col2:

        feature_html = "\n".join([
            '<div class="feature">',
            '<div class="feature-icon">📝</div>',
            '<div class="feature-title">Summarize Notes</div>',
            '<div class="feature-text">',
            'Turn long study notes into concise summaries and key points.',
            '</div>',
            '</div>'
        ])

        st.markdown(feature_html, unsafe_allow_html=True)

    st.write("")

    col3, col4 = st.columns(2)

    with col3:

        feature_html = "\n".join([
            '<div class="feature">',
            '<div class="feature-icon">🧠</div>',
            '<div class="feature-title">Generate Quiz</div>',
            '<div class="feature-text">',
            'Create practice MCQs automatically from any study topic.',
            '</div>',
            '</div>'
        ])

        st.markdown(feature_html, unsafe_allow_html=True)

    with col4:

        feature_html = "\n".join([
            '<div class="feature">',
            '<div class="feature-icon">🤖</div>',
            '<div class="feature-title">Ask AI</div>',
            '<div class="feature-text">',
            'Ask StudyGenie academic questions and get clear answers.',
            '</div>',
            '</div>'
        ])

        st.markdown(feature_html, unsafe_allow_html=True)

    st.divider()

    # --------------------------------------------------------
    # STUDY ASSISTANT
    # --------------------------------------------------------

    st.markdown(
        '<div class="small-label">AI STUDY ASSISTANT</div>',
        unsafe_allow_html=True
    )

    feature = st.selectbox(
        "Choose a study tool",
        [
            "Explain a Topic",
            "Summarize Notes",
            "Generate Quiz",
            "Ask AI"
        ],
        key="feature"
    )

    # --------------------------------------------------------
    # INPUT SETTINGS
    # --------------------------------------------------------

    if feature == "Explain a Topic":

        input_label = "What topic would you like me to explain?"

        placeholder = (
            "Example: Explain machine learning in simple language"
        )

    elif feature == "Summarize Notes":

        input_label = "Paste your study notes here"

        placeholder = (
            "Paste your notes, textbook content, or study material..."
        )

    elif feature == "Generate Quiz":

        input_label = "Enter a topic for your quiz"

        placeholder = "Example: Data Structures"

    else:

        input_label = "Ask StudyGenie a question"

        placeholder = (
            "Example: What is the difference between AI and ML?"
        )

    user_input = st.text_area(
        input_label,
        placeholder=placeholder,
        height=170,
        key="study_input"
    )

    # --------------------------------------------------------
    # GENERATE
    # --------------------------------------------------------

    if st.button(
        "✨ Generate with StudyGenie",
        use_container_width=True,
        key="generate"
    ):

        if not api_key or not client:

            st.error(
                "Gemini API key not found. Please check your .env file."
            )

        elif not user_input.strip():

            st.warning(
                "Please enter a topic, question, or notes first."
            )

        else:

            # ----------------------------------------------
            # EXPLAIN PROMPT
            # ----------------------------------------------

            if feature == "Explain a Topic":

                prompt = (
                    "You are StudyGenie, an AI study assistant.\n\n"
                    "Explain the following topic to a college student "
                    "using simple and easy-to-understand language.\n\n"
                    "Topic:\n"
                    + user_input
                    + "\n\n"
                    "Structure the answer as:\n"
                    "1. Simple Definition\n"
                    "2. Main Points\n"
                    "3. Easy Example\n"
                    "4. Short Summary\n\n"
                    "Avoid unnecessary complexity."
                )

            # ----------------------------------------------
            # SUMMARY PROMPT
            # ----------------------------------------------

            elif feature == "Summarize Notes":

                prompt = (
                    "You are StudyGenie, an AI study assistant.\n\n"
                    "Summarize the following study notes for a college student.\n\n"
                    "Notes:\n"
                    + user_input
                    + "\n\n"
                    "Provide:\n"
                    "1. Short Summary\n"
                    "2. Important Key Points\n"
                    "3. Important Terms\n"
                    "4. Quick Revision Points\n\n"
                    "Keep the information clear and useful for exam preparation."
                )

            # ----------------------------------------------
            # QUIZ PROMPT
            # ----------------------------------------------

            elif feature == "Generate Quiz":

                prompt = (
                    "You are StudyGenie, an AI study assistant.\n\n"
                    "Create 5 multiple-choice questions for a college student "
                    "based on this topic:\n\n"
                    + user_input
                    + "\n\n"
                    "For every question provide:\n"
                    "Question\n"
                    "A. Option\n"
                    "B. Option\n"
                    "C. Option\n"
                    "D. Option\n"
                    "Correct Answer\n"
                    "Short Explanation\n\n"
                    "Make the questions educational and relevant."
                )

            # ----------------------------------------------
            # ASK AI PROMPT
            # ----------------------------------------------

            else:

                prompt = (
                    "You are StudyGenie, an AI study assistant.\n\n"
                    "Answer the student's question clearly and accurately.\n\n"
                    "Question:\n"
                    + user_input
                    + "\n\n"
                    "Use simple language. "
                    "Give an example when useful. "
                    "Structure the answer clearly."
                )

            # ----------------------------------------------
            # CALL AI
            # ----------------------------------------------

            with st.spinner("StudyGenie is thinking... 🤖"):

                try:

                    response = client.models.generate_content(
                        model="gemma-4-31b-it",
                        contents=prompt
                    )

                    st.session_state.result = response.text

                    st.success(
                        "StudyGenie generated your answer successfully! ✨"
                    )

                except Exception as e:

                    error_message = str(e)

                    if "503" in error_message:

                        st.warning(
                            "The AI service is temporarily busy. "
                            "Please wait a few seconds and try again."
                        )

                    else:

                        st.error(
                            "Something went wrong: "
                            + error_message
                        )

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    if st.session_state.result:

        st.divider()

        st.markdown(
            '<div class="small-label">AI-GENERATED RESULT</div>',
            unsafe_allow_html=True
        )

        result_html = "\n".join([
            '<div class="result">',
            '</div>'
        ])

        st.markdown(result_html, unsafe_allow_html=True)

        st.markdown(st.session_state.result)

        st.write("")

        if st.button(
            "↻ Start New Study Session",
            use_container_width=True,
            key="new_session"
        ):

            st.session_state.result = ""
            st.rerun()

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer">StudyGenie • AI-Powered Study Assistant</div>',
    unsafe_allow_html=True
)