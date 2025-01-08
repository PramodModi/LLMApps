import streamlit as st
from graph.Graph import getChat_to_image

#******************************************
# Setting up streamlit UI
#******************************************

st.set_page_config(
    page_title="Image Processing",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="auto",
)

#st.header("Chat With Your Image")
st.markdown(
    """
    <h1 style="text-align: center; color: blue; font-size: 36px;">
        Chat With Your Image
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
# Upload Image File from UI
#******************************************
# File uploader
image_path = st.file_uploader("Choose a file", type=["jpeg", "jpg", "png"])

#******************************************
# Calling LLM with Input Query
#******************************************

if query := st.chat_input(placeholder="Enter your query.."):
    if image_path is None:
        st.warning("Please upload an Image to proceed!")
    else:
        # Display user message in chat message container
        st.chat_message("user").markdown(query)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": query})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = getChat_to_image(image_path, query=query)
            #response = st.write(run_llm(image_path, query=query))
            st.write(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

# Add a footer
st.markdown("---")
#st.markdown("Powered by Pramod Modi")