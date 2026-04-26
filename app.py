import streamlit as st
from google import genai
import os


client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

for m in client.models.list():
    print(m.name)


st.set_page_config(page_title="TUHIN App")
st.title("  🤖 AI Assistant")


if "messages" not in st.session_state:
    st.session_state.messages = []


for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


user_input = st.chat_input("Ask me anything...")

if user_input:

    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_input
    )
    reply = response.text

    # Show assistant reply
    st.chat_message("assistant").write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})