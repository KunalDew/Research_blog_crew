from pathlib import Path

import streamlit as st
from crewai.project import load_crew
from dotenv import load_dotenv

load_dotenv()

CREW_FILE = Path(__file__).with_name("crew.jsonc")

st.set_page_config(page_title="Research Blog Crew", page_icon="📝", layout="wide")
st.title("📝 Research Blog Crew")
st.caption("A Researcher agent gathers facts, then a Writer agent turns them into a blog post.")

with st.sidebar:
    st.header("How it works")
    st.markdown(
        "1. **Researcher** searches and compiles notes\n"
        "2. **Writer** drafts the blog post from those notes\n\n"
        "Tasks run sequentially."
    )

topic = st.text_input("Blog topic", placeholder="e.g. The future of solar energy")
run = st.button("Generate blog post", type="primary", disabled=not topic.strip())

if run:
    try:
        crew, default_inputs = load_crew(CREW_FILE)
        with st.spinner("Researcher and Writer are working... this can take a few minutes."):
            result = crew.kickoff(inputs={**default_inputs, "topic": topic.strip()})
        st.session_state["result"] = result
        st.session_state["topic"] = topic.strip()
    except Exception as e:
        st.error(f"Something went wrong: {e}")

result = st.session_state.get("result")
if result:
    st.success("Done!")
    post_tab, research_tab = st.tabs(["✍️ Blog post", "🔎 Research notes"])

    with post_tab:
        st.markdown(result.raw)
        st.download_button(
            "Download as Markdown",
            data=result.raw,
            file_name="blog_post.md",
            mime="text/markdown",
        )

    with research_tab:
        if result.tasks_output:
            st.markdown(result.tasks_output[0].raw)
