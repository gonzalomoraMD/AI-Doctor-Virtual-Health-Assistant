import streamlit as st
import requests

st.title("🩺 AI Doctor - Virtual Health Assistant")

user_input = st.text_input("Type your symptoms here:")

if st.button("Ask Doctor"):
    response = requests.post("http://127.0.0.1:8000/chat", params={"user_input": user_input}).json()
    st.write("👨‍⚕️ Doctor:", response["response"])

if st.button("Start Voice Chat"):
    voice_response = requests.post("http://127.0.0.1:8000/voice").json()
    st.write("🎙 Doctor:", voice_response["response"])
