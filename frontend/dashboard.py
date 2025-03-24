import streamlit as st
import requests

# Dashboard Title
st.title("CareerPath AI – Interactive Dashboard")

# Sidebar for Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Career Recommendations", "Job Market Trends", "Roadmap to Success", "Resume Optimization"])

# Backend API URL
BACKEND_URL = "http://127.0.0.1:5000"

# Home Page
if page == "Home":
    st.header("Welcome to CareerPath AI!")
    st.write("""
    CareerPath AI is your personalized career navigator. It helps you:
    - Discover the best career paths based on your skills and interests.
    - Explore job market trends and in-demand careers.
    - Get a step-by-step roadmap to achieve your career goals.
    - Optimize your resume and LinkedIn profile.
    """)

# Career Recommendations Page
elif page == "Career Recommendations":
    st.header("Career Recommendations")
    st.write("Get personalized career suggestions based on your skills, interests, and academic background.")

    # Input fields
    skills = st.text_input("Enter your skills (e.g., Programming, Writing):")
    interests = st.text_input("Enter your interests (e.g., Technology, Literature):")
    academic_background = st.text_input("Enter your academic background (e.g., Computer Science, English):")

    if st.button("Get Recommendations"):
        if skills and interests and academic_background:
            try:
                response = requests.post(
                    f"{BACKEND_URL}/recommend",
                    json={"skills": skills, "interests": interests, "academic_background": academic_background},
                    timeout=5
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
                    st.error(f"Error: {response.json().get('error', 'Unknown error')}")
            except requests.exceptions.ConnectionError:
                st.error("Backend is not running. Please start the Flask server.")
            except requests.exceptions.Timeout:
                st.error("The request timed out. Try again later.")
        else:
            st.warning("Please fill in all fields.")

# Job Market Trends Page
elif page == "Job Market Trends":
    st.header("Job Market Trends")
    st.write("Explore real-time job market trends and in-demand careers.")

    if st.button("View Trends"):
        try:
            response = requests.get(f"{BACKEND_URL}/job_market", timeout=5)
            if response.status_code == 200:
                trends = response.json().get("trends", [])
                if trends:
                    st.success("Job Market Trends:")
                    for trend in trends:
                        st.write(f"""
                        - **Job Title:** {trend['job_title']}
                        - **Demand Level:** {trend['demand_level']}
                        - **Salary Range:** {trend['salary_range']}
                        - **Experience_Level:** {trend['experience_level']}
                        """)
                else:
                    st.warning("No job market trends found.")
            else:
                st.error(f"Error: {response.json().get('error', 'Unknown error')}")
        except requests.exceptions.ConnectionError:
            st.error("Backend is not running. Please start the Flask server.")
        except requests.exceptions.Timeout:
            st.error("The request timed out. Try again later.")

# Roadmap to Success Page
elif page == "Roadmap to Success":
    st.header("Roadmap to Success")
    st.write("Get a step-by-step guide to achieve your career goals.")

    career = st.text_input("Enter your desired career (e.g., Software Engineer, Content Writer):")
    if st.button("Generate Roadmap"):
        if career:
            try:
                response = requests.post(f"{BACKEND_URL}/roadmap", json={"career": career}, timeout=5)
                if response.status_code == 200:
                    roadmap = response.json().get("roadmap", [])
                    if roadmap:
                        st.success(f"Roadmap for {career}:")
                        for step in roadmap:
                            st.write(f"- {step}")
                    else:
                        st.warning("No roadmap found for this career.")
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error')}")
            except requests.exceptions.ConnectionError:
                st.error("Backend is not running. Please start the Flask server.")
            except requests.exceptions.Timeout:
                st.error("The request timed out. Try again later.")
        else:
            st.warning("Please enter a career.")

# Resume Optimization Page
elif page == "Resume Optimization":
    st.header("Resume Optimization")
    st.write("Optimize your resume using AI-powered suggestions.")

    resume_text = st.text_area("Paste your resume text here:")
    if st.button("Optimize Resume"):
        if resume_text:
            try:
                response = requests.post(f"{BACKEND_URL}/optimize_resume", json={"resume_text": resume_text}, timeout=5)
                if response.status_code == 200:
                    optimized_text = response.json().get("optimized_resume", "")
                    st.success("Optimized Resume:")
                    st.write(optimized_text)
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error')}")
            except requests.exceptions.ConnectionError:
                st.error("Backend is not running. Please start the Flask server.")
            except requests.exceptions.Timeout:
                st.error("The request timed out. Try again later.")
        else:
            st.warning("Please paste your resume text.")
