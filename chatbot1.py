import openai
import streamlit as st
from streamlit_chat import message

# Make a request to the ChatCompletion API
SECRET_KEY = os.environ.get("mykey")
openai.api_key = SECRET_KEY

start_sequence = "\nAI:"
restart_sequence = "\nHuman: "

# Initialize a list to store the conversation history
previous_messages = []


def chatbot(question):
    # define the conversation context based on the input question and the previous messages
    if "world series" in question:
        messages = [
            {"role": "system", "content": "You are a helpful assistant created by Barry."},
            {"role": "user", "content": question},
            {"role": "assistant",
                "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": "Where was it played?"}
        ]
    else:
        # default conversation context if question doesn't match any specific case
        messages = [
            {"role": "system", "content": "You are a helpful assistant created by Barry."},
            {"role": "user", "content": question}
        ]
    # append the previous messages to the conversation context
    messages.extend(previous_messages)

    # generating the response based on the conversation context
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.1,
        presence_penalty=0.6,
        stop=[" Human:", "AI:"]
    )

    # return the generated response
    return response["choices"][0]["message"]["content"]


# Set up Streamlit app
st.title("JRZY Chatbot")
st.subheader("I'm ready to talk about sports. Are you?")

# Initialize session state for message history
if "message_history" not in st.session_state:
    st.session_state.message_history = []

placeholder = st.sidebar.empty()  # a placeholder container to display the messages

question = st.text_input("Ask me your questions:", "")

if st.button("Ask"):
    response = chatbot(question)  # get response from the chatbot

    # append the user's question and the chatbot's response to the message history
    st.session_state.message_history.append(question)
    st.session_state.message_history.append(response)

    # append the user's question and the chatbot's response to the previous messages list
    previous_messages.append({"role": "user", "content": question})
    previous_messages.append({"role": "assistant", "content": response})

    # display the message history using the placeholder container
    with placeholder.container():
        for msg in st.session_state.message_history:
            # check if the message is from the user or the chatbot
            if msg == question or msg.startswith("You:"):
                message(msg, is_user=True)  # display the user's message
            else:
                message(msg, is_user=False)  # display the chatbot's message


def message(msg, is_user):
    if is_user:
        st.write(
            f'<div style="text-align: right; color: blue;">You: {msg}</div>', unsafe_allow_html=True)
    else:
        st.write(
            f'<div style="text-align: left; color: green;">Chatbot: {msg}</div>', unsafe_allow_html=True)
    st.write('<br>', unsafe_allow_html=True)
