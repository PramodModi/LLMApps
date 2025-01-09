import streamlit as st
from datetime import date, time, datetime

from nltk import align

from graph.Graph import run_graph

#******************************************
# Setting up streamlit UI
#******************************************

st.set_page_config(
    page_title="Ask Astrologer",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="auto",
)

#st.header("Chat With Your Image")

st.markdown(
    """
    <h1 style="text-align: center; color: blue; font-size: 36px;">
        Ask Astrologer
    </h1>
    """,
    unsafe_allow_html=True,
)

# Custom CSS for dark theme and modern look
st.markdown(
    """
<style>
    .stApp {
        background-color: #E0E0E0;
        color: #004C99;
    }
    .stMarkdown{
        color: #004C99;
    } 
    .stImage{
        alignment : center;
    } 
</style>
""",
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#******************************************
# Input
#******************************************
st.sidebar.title("Required Details")
# Date of Birth Input
dob = st.sidebar.date_input(
    "Select your Date of Birth:",
    value=date(2000, 1, 1),  # Default date shown
    min_value=date(1950, 1, 1),  # Minimum selectable date
    max_value=date.today()  # Maximum selectable date (current date)
)

# Gender Selection
gender = st.sidebar.radio("Select your Gender:", ["Male", "Female"])


# Time Input: Allow manual input with validation
time_of_birth_str = st.sidebar.text_input("Enter the Time of Birth (HH:MM):", value="12:00")
try:
    time_of_birth = datetime.strptime(time_of_birth_str, "%H:%M").time()
except ValueError:
    st.sidebar.error("Invalid time format! Please use HH:MM (e.g., 12:30).")
    time_of_birth = None

# Location Input
location = st.sidebar.text_input("Enter your Location of Birth:")

#******************************************
# Calling LLM with Input Query
#******************************************

if query := st.chat_input(placeholder="Enter your query.."):
    if dob is None:
        st.error("Please provide Date Of Birth")
    elif gender is None:
        st.error("Please Select Gender")
    elif time_of_birth is None:
        st.error("Please provide Time of birth")
    elif location is None:
        st.error("Please provide Location of birth")
    else:
        # Prepare info
        info = {"Date of birth": dob,
                "Time of birth": time_of_birth,
                "Location": location,
                "Sex": gender
                }
        # Display user message in chat message container
        st.chat_message("user").markdown(query)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": query})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = run_graph(info, query=query)
            #response = st.write(run_llm(image_path, query=query))
            st.write(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

# Add a footer
st.markdown("---")
#st.markdown("Powered by Pramod Modi")