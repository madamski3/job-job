"""
Streamlit App for Job Search AI
"""

import streamlit as st
import os
from job_job import JobSearchAI
import config

# Page configuration
st.set_page_config(
    page_title="JobJob the Jobot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'job_ai' not in st.session_state:
    st.session_state.job_ai = JobSearchAI()

if 'documents_uploaded' not in st.session_state:
    st.session_state.documents_uploaded = False

def main():
    st.title("🤖 Hi, I'm JobJob! Let me help you get a job!")
    st.markdown("Really I'm just happy to be here! :)")
    
    # Check if API key is set
    if not config.OPENAI_API_KEY:
        st.error("⚠️ Please set your OpenAI API key in the .env file")
        st.stop()
    
        # Sidebar
    with st.sidebar:
        # Resume Management Section
        st.header("📰 Resume")
        
        # Document upload
        uploaded_files = st.file_uploader(
            "Upload Resume & Documents",
            type=['pdf', 'txt', 'md'],
            accept_multiple_files=True,
            help="Upload your resume and information about your professional experience"
        )
        
        if uploaded_files:
            if st.button("Upload"):
                with st.spinner("Document upload in progress..."):
                    file_paths = []
                    for uploaded_file in uploaded_files:
                        file_path = st.session_state.job_ai.document_manager.save_uploaded_file(uploaded_file)
                        file_paths.append(file_path)
                    
                    st.session_state.job_ai.add_documents(file_paths)
                    st.session_state.documents_uploaded = True
                    st.success(f"Successfully processed {len(uploaded_files)} documents!")
        
        # Document status
        chunk_count = st.session_state.job_ai.get_document_count()
        doc_count = st.session_state.job_ai.document_manager.get_document_count()
        if doc_count > 0:
            st.success(f"📄 {doc_count} documents uploaded")
        else:
            st.warning("No documents loaded yet")
        
        st.divider()
        
        # Personal Context Management Section
        st.header("👤 Personal Context Files")
        st.markdown("Background information used to personalize responses.")
        
        # List files from background folder
        background_dir = os.path.join("context", "background")
        if os.path.exists(background_dir):
            files = [f for f in os.listdir(background_dir) if f.endswith('.txt')]
            if files:
                for file in files:
                    with open(os.path.join(background_dir, file), 'r') as f:
                        content = f.read()
                    with st.expander(f"📄 {file}"):
                        st.text(content)
            else:
                st.info("No context files found in background folder")
        
        st.divider()
        
        # Clear all data button at bottom of sidebar
        if st.button("🗑️ Clear All Data"):
            st.session_state.job_ai.clear_all_data()
            st.session_state.documents_uploaded = False
            st.success("All data cleared!")
            st.rerun()
    
    # Main content area
    if not st.session_state.documents_uploaded and st.session_state.job_ai.get_document_count() == 0:
        st.info("👆 Please upload your resume and experience documents in the sidebar to get started.")
        return
    
    # Tab navigation
    tab1, tab2, tab3 = st.tabs([
        "📝 Resume Optimizer",
        "🎤 Interview Prep", 
        "📋 Application Questions"
    ])
    
    with tab1:
        resume_optimizer_tab()
    
    with tab2:
        interview_prep_tab()
    
    with tab3:
        application_questions_tab()

def resume_optimizer_tab():
    st.header("📝 Resume Optimizer")
    st.markdown("Get personalized suggestions to tailor your resume for specific jobs.")
    
    job_description = st.text_area(
        "Paste the job description here:",
        height=200,
        help="Copy and paste the full job description for best results"
    )
    
    specific_sections = st.text_input(
        "Focus on specific sections (optional):",
        placeholder="e.g., technical skills, work experience, projects"
    )
    
    if st.button("🚀 Optimize Resume", type="primary"):
        if job_description.strip():
            with st.spinner("Analyzing job requirements and optimizing your resume..."):
                result = st.session_state.job_ai.optimize_resume(job_description, specific_sections)
                st.markdown("### 📋 Optimization Recommendations")
                st.markdown(result)
        else:
            st.warning("Please enter a job description first.")

def interview_prep_tab():
    st.header("🎤 Interview Preparation")
    st.markdown("Practice with likely interview questions tailored to your background.")
    
    job_description = st.text_area(
        "Job Description:",
        height=150,
        help="Enter the job description to generate relevant interview questions"
    )
    
    interview_type = st.selectbox(
        "Interview Type:",
        ["General", "Technical", "Behavioral", "Leadership", "Phone/Video"]
    )
    
    if st.button("🎯 Generate Interview Questions", type="primary"):
        if job_description.strip():
            with st.spinner("Preparing interview questions and answers..."):
                result = st.session_state.job_ai.prepare_interview_questions(
                    job_description, interview_type.lower()
                )
                st.markdown("### 🎤 Interview Preparation Guide")
                st.markdown(result)
        else:
            st.warning("Please enter a job description first.")

def application_questions_tab():
    st.header("📋 Application Question Responses")
    st.markdown("Get help drafting responses to job application questions.")
    
    question = st.text_area(
        "Application Question:",
        height=100,
        placeholder="e.g., Why are you interested in this position? Describe a challenging project you worked on. What are your career goals?"
    )
    
    job_description = st.text_area(
        "Job Description (optional but recommended):",
        height=150,
        help="Including the job description helps tailor your response to the specific role"
    )
    
    if st.button("✍️ Draft Response", type="primary"):
        if question.strip():
            with st.spinner("Crafting your application response..."):
                result = st.session_state.job_ai.draft_application_response(question, job_description)
                st.markdown("### 📝 Your Response")
                st.markdown(result)
        else:
            st.warning("Please enter the application question first.")

if __name__ == "__main__":
    main()