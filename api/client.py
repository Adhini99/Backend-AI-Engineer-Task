import requests
import streamlit as st

API_URL = "http://localhost:8000/generate-post"

def get_post(topic):
    response = requests.post(API_URL, json={"topic": topic})
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.json()}

# Streamlit UI
st.title("LinkedIn Post Generator (Gemini + Tavily)")

topic = st.text_input("Enter a topic")

if st.button("Generate Post"):
    result = get_post(topic)
    if "error" in result:
        st.error(result["error"])
    else:
        st.subheader("LinkedIn Post")
        st.write(result["linkedin_post"])
        st.subheader("News Sources")
        for url in result["news_sources"]:
            st.markdown(f"- [{url}]({url})")
