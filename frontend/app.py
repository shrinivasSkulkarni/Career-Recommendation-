import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:5000"

st.title("CareerPath AI – Career Recommendation System")

# Input fields
skills = st.text_input("Enter your skills (e.g., Programming, Writing):")
interests = st.text_input("Enter your interests (e.g., Technology, Literature):")
academic_background = st.text_input("Enter your academic background (e.g., Bachelor's, Masters's, Phd):")

if st.button("Get Recommendations"):
    if skills and interests and academic_background:
        try:
            response = requests.post(
                f"{BACKEND_URL}/recommend",
                json={"skills": skills, "interests": interests, "academic_background": academic_background},
                timeout=5  # Prevent long waiting times
            )

            if response.status_code == 200:
                recommendations = response.json().get("recommendations", [])
                if recommendations:
                    st.success("Your Career Recommendations:")
                    for career in recommendations:
                        st.write(f"- {career}")
                else:
                    st.warning("No recommendations found.")
            else:
                st.error(f"Error from backend: {response.json().get('error', 'Unknown error')}")
        except requests.exceptions.ConnectionError:
            st.error("Backend is not running. Please start the Flask server.")
        except requests.exceptions.Timeout:
            st.error("The request timed out. Try again later.")
    else:
        st.warning("Please fill in all fields.")

st.divider()
st.subheader("Career Copilot")
st.write("Ask questions about your resume and get answers with sources.")

copilot_q = st.text_input("Ask about your resume or a job description", key="copilot_q")

if st.button("Ask Copilot", key="copilot_btn") and copilot_q:
    try:
        with st.spinner("Thinking..."):
            r = requests.post("http://127.0.0.1:8000/ask", json={"question": copilot_q}, timeout=60)
            r.raise_for_status()
            res = r.json()
        st.write(res["answer"])
        with st.expander("Sources"):
            for s in res["sources"]:
                st.caption(s["text"])
    except Exception as e:
        st.error(f"Copilot service not reachable: {e}")