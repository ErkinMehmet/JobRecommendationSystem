import streamlit as st
from src.helper import extract_text_from_pdf, ask_openai, fetch_linkedin_jobs,fetch_naukri_jobs

def main():
    st.set_page_config(page_title="Job Recommendation System", page_icon=":briefcase:",layout="wide")
    st.title("AI Job Recommendation System")
    st.markdown("Upload your CV and get job recommendations based on your skills and experience.")
    uploaded_file = st.file_uploader("Upload your CV (PDF format)", type=["pdf"])
    if uploaded_file is not None:
        with st.spinner("Processing your CV..."):
            cv_text=extract_text_from_pdf(uploaded_file)

        with st.spinner("Summarizing your CV..."):
            summary_prompt=f"Summarize the following resume highlighting the skills, education and experience:\n\n{cv_text}"
            cv_summary=ask_openai(summary_prompt,max_tokens=500)

        with st.spinner("Finding skill gaps"):
            gaps=ask_openai(f"Analyze this resume and highlight missing skills, certifications, and experiences needed for better job opportunities:\n\n{cv_summary}",max_tokens=400)
        with st.spinner("Creating Future Roadmap..."):
            roadmap = ask_openai(f"Based on this resume, suggest a future roadmap to improve this person's career prospects (Skill to learn, certification needed, industry exposure): \n\n{resume_text}", max_tokens=400)
        
        # display nicely formatted results
        st.markdown("---")
        st.header("📑 Resume Summary")
        st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{summary}</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.header("🛠️ Skill Gaps & Missing Areas")
        st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{gaps}</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.header("🚀 Future Roadmap & Preparation Strategy")
        st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{roadmap}</div>", unsafe_allow_html=True)

        st.success("CV processed successfully!")

        if st.button("Find Job Recommendations"):
            with st.spinner("Fetching job recommendations..."):
                keywords = ask_openai(
                f"Based on this resume summary, suggest the best job titles and keywords for searching jobs. Give a comma-separated list only, no explanation.\n\nSummary: {summary}",
                max_tokens=100
            )
            search_keywords_clean=keywords.replace("\n","").strip()
            st.success(f"Extracted Job Keywords: {search_keywords_clean}")
            with st.spinner("Searching for jobs on LinkedIn and Naukri..."):
                l_jobs = fetch_linkedin_jobs(query=search_keywords_clean  ,  limit=60)
                n_jobs = fetch_naukri_jobs(query=search_keywords_clean  ,  limit=60)

            st.markdown("---")
            st.header("💼 Top LinkedIn Jobs")
            if l_jobs:
                for job in l_jobs:
                    st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
                    st.markdown(f"- 📍 {job.get('location')}")
                    st.markdown(f"- 🔗 [View Job]({job.get('link')})")
                    st.markdown("---")
            else:
                st.warning("No LinkedIn jobs found.")

            st.markdown("---")
            st.header("💼 Top Naukri Jobs")
            if l_jobs:
                for job in l_jobs:
                    st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
                    st.markdown(f"- 📍 {job.get('location')}")
                    st.markdown(f"- 🔗 [View Job]({job.get('url')})")
                    st.markdown("---")
            else:
                st.warning("No Naukri jobs found.")

if __name__ == "__main__":
    main()