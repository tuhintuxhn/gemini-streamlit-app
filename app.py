import streamlit as st
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

    #voice input
    audio = st.audio_input("🎙️ Speak your message")

    if audio:
        st.chat_message("user").write("🎙️ Voice message sent")
        st.session_state.messages.append({"role": "user", "content": "🎙️ Voice message sent"})

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Respond to this audio message: please reply in text"
        )
        reply = response.text
        st.chat_message("assistant").write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})


#text and file input

user_input = st.chat_input("Ask me anything...", accept_file=True, file_type=["png", "jpg", "jpeg", "pdf", "txt"])

if user_input:
    prompt = str(user_input["text"]) if user_input["text"] else ""
    files = user_input["files"]

    st.chat_message("user").write(prompt if prompt else "📎 File sent")
    st.session_state.messages.append({"role": "user", "content": prompt if prompt else "📎 File sent"})

    if files:
        image = PIL.Image.open(files[0])
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[{"text": prompt}, {"inline_data": {"mime_type": "image/jpeg", "data": files[0].getvalue()}}]
        )
    else:
         response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[{"text": prompt}]
    )
    reply = response.text
    st.chat_message("assistant").write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})