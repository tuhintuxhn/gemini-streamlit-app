import streamlit as st
from click import prompt
from google import genai
import os
import PIL.Image


client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

for m in client.models.list():
    print(m.name)


st.set_page_config(page_title="TUHIN App")
st.title("  🤖 AI Assistant")


if "messages" not in st.session_state:
    st.session_state.messages = []


for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_input = st.chat_input("Ask me anything...", accept_file=True, file_type=["png", "jpg", "jpeg", "pdf", "txt"])

if user_input:
    prompt = user_input.text
    files = user_input.files

    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    if files:
        image = PIL.Image.open(files[0])
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[user_input, image]
        )
    else:
         response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_input
    )
    reply = response.text
    st.chat_message("assistant").write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})