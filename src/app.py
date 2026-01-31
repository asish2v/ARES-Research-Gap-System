import streamlit as st
import json
import os
import subprocess

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="ARES • Research Gap Intelligence",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# CUSTOM CSS (100× UI)
# =========================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

.main-title {
    font-size: 3rem;
    font-weight: 800;
    color: #ffffff;
}

.subtitle {
    font-size: 1.2rem;
    color: #cfd8dc;
    margin-bottom: 2rem;
}

.card {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 18px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
    backdrop-filter: blur(10px);
}

.badge {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 999px;
    font-weight: 600;
    color: white;
    background: linear-gradient(90deg, #ff416c, #ff4b2b);
    margin-bottom: 12px;
}

.keyword {
    display: inline-block;
    padding: 6px 12px;
    margin: 4px;
    background: rgba(0, 123, 255, 0.15);
    border-radius: 999px;
    color: #90caf9;
    font-size: 0.9rem;
}

.footer {
    text-align: center;
    color: #90a4ae;
    margin-top: 40px;
    font-size: 0.85rem;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("<div class='main-title'>🔍 ARES</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>AI-Driven Research Gap Intelligence System</div>",
    unsafe_allow_html=True
)

# =========================
# METRICS DASHBOARD
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("📄 Papers Analyzed", "5")
col2.metric("🧠 Topics Discovered", "3")
col3.metric("🚨 Research Gaps", "1")

st.divider()

# =========================
# RUN ANALYSIS BUTTON
# =========================
if st.button("🚀 Run Research Gap Analysis", use_container_width=True):
    with st.spinner("Running AI analysis on research papers..."):
        subprocess.run(["python", "src/topic_modeling.py"])
    st.success("Analysis completed successfully!")

# =========================
# LOAD RESULTS
# =========================
RESULT_PATH = "data/final_results/research_gap_report.json"

def load_results():
    if not os.path.exists(RESULT_PATH):
        return None
    with open(RESULT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

results = load_results()

# =========================
# DISPLAY GAPS
# =========================
if results:
    st.divider()
    st.markdown("## 📌 Identified Research Gaps")

    for gap in results:
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.markdown("<div class='badge'>HIGH IMPACT GAP</div>", unsafe_allow_html=True)
        st.markdown(f"### 🧠 Topic {gap['topic_id']}")

        st.markdown("**Keywords**")
        for kw in gap["keywords"]:
            st.markdown(f"<span class='keyword'>{kw}</span>", unsafe_allow_html=True)

        st.markdown("### 📖 Research Insight")
        st.info(gap["gap_explanation"])

        st.markdown("</div>", unsafe_allow_html=True)

    st.download_button(
        "📥 Download Research Gap Report (JSON)",
        data=json.dumps(results, indent=4),
        file_name="ARES_Research_Gap_Report.json",
        mime="application/json",
        use_container_width=True
    )

else:
    st.warning("No analysis results found. Please run the analysis first.")

# =========================
# FOOTER
# =========================
st.markdown(
    "<div class='footer'>ARES © AI-Driven Research Gap Discovery System</div>",
    unsafe_allow_html=True
)
