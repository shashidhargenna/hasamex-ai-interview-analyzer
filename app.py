import streamlit as st

from src.qa import answer_question
from src.guide_analysis import analyze_interview_guide
from src.theme_analysis import analyze_themes_and_disagreements


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Hasamex Expert Interview Analyzer",
    page_icon="🔎",
    layout="wide"
)


# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("🔎 Hasamex Expert Interview Analyzer")

st.write(
    "Analyze three expert interviews on the European robotic "
    "surgery market using transcript-grounded AI."
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select an analysis",
    [
        "Interview Guide",
        "Ask Across Transcripts",
        "Themes & Differences",
    ]
)


# ==================================================
# 1. INTERVIEW GUIDE
# ==================================================

if page == "Interview Guide":

    st.header("📋 Interview Guide Analysis")

    st.write(
        "Answers to the six questions in the interview guide, "
        "with supporting expert evidence."
    )

    if st.button("Analyze Interview Guide"):

        with st.spinner("Analyzing interview guide..."):

            results = analyze_interview_guide()

        for index, result in enumerate(results, start=1):

            st.subheader(
                f"Question {index}: {result['question']}"
            )

            st.markdown("### Answer")

            st.write(result["answer"])

            st.markdown("### Supporting Evidence")

            for evidence in result["evidence"]:

                with st.expander(
                    f"{evidence.expert} — "
                    f"{evidence.market} — "
                    f"{evidence.timestamp}"
                ):

                    st.write("**Exact Quote:**")

                    st.write(
                        f'"{evidence.quote}"'
                    )

                    st.write(
                        f"**Segment ID:** {evidence.segment_id}"
                    )

            st.divider()


# ==================================================
# 2. ASK ACROSS TRANSCRIPTS
# ==================================================

elif page == "Ask Across Transcripts":

    st.header("🔍 Ask Across Transcripts")

    st.write(
        "Ask a question and retrieve evidence from the "
        "expert interviews."
    )

    question = st.text_area(
        "Enter your question",
        placeholder=(
            "Example: What are the main barriers "
            "to robotic surgery adoption?"
        ),
        height=100
    )

    if st.button("Ask Question"):

        if not question.strip():

            st.warning("Please enter a question.")

        else:

            with st.spinner("Searching transcripts..."):

                answer, evidence = answer_question(
                    question=question,
                    k=6
                )

            st.markdown("### Answer")

            st.write(answer)

            st.markdown("### Supporting Evidence")

            for item in evidence:

                with st.expander(
                    f"{item.expert} — "
                    f"{item.market} — "
                    f"{item.timestamp}"
                ):

                    st.write("**Exact Quote:**")

                    st.write(
                        f'"{item.quote}"'
                    )

                    st.write(
                        f"**Segment ID:** {item.segment_id}"
                    )


# ==================================================
# 3. THEMES & DIFFERENCES
# ==================================================

elif page == "Themes & Differences":

    st.header("📊 Common Themes & Differences")

    st.write(
        "Identify common themes and differences across "
        "the three expert interviews."
    )

    if st.button("Analyze Themes & Differences"):

        with st.spinner(
            "Analyzing themes and differences..."
        ):

            result = analyze_themes_and_disagreements()

        st.markdown("### Analysis")

        st.write(result["analysis"])