from openai import OpenAI
import streamlit as st
import os

openai_api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# Titles
st.set_page_config(page_title="General AI Chatbot")
st.markdown("# General AI Chatbot")
st.sidebar.header("General AI Chatbot")
st.write("This demo helps you figure out general questions. Enjoy!")

text = st.text_area('Enter your question:',
                    'What are the three key pieces of advice for learning how to code?',
                    key="user_text")

def get_response(question):
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # Specify the model, adjust if a different version is desired
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

if st.button('Ask'):
    if text:
        response = get_response(text)
        st.text_area("Answer", value=response, height=150, key="response")
    else:
        st.warning("Please enter a question to get an answer.")
