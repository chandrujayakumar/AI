import streamlit as st
import concurrent.futures

from utils.pdf_loader import extract_text
from utils.planner import plan_agents, risk_score
from utils.agents import analyze_with_role, generate_final_report
from utils.agents import ai_risk_assessment
from utils.vector_store import store_contract, query_relevant_chunks

st.title("ClauseAI – Multi-Agent Contract Analyzer")

uploaded_file = st.file_uploader("Upload Contract PDF", type=["pdf"])

if uploaded_file:
    
    text = extract_text(uploaded_file)
    store_contract(text)

    st.text_area(
        label="Extracted Contract Text",
        value=text[:2000],
        height=250,
        label_visibility="collapsed"
    )

    if st.button("Generate AI Multi-Agent Report"):

        with st.spinner("Analyzing contract using AI agents..."):

            # Planning
            plan = plan_agents(text)

            # Agent Analyses
            with concurrent.futures.ThreadPoolExecutor() as executor:

                future_compliance = executor.submit(analyze_with_role, "Compliance", plan["compliance"])
                future_finance = executor.submit(analyze_with_role, "Finance", plan["finance"])
                future_legal = executor.submit(analyze_with_role, "Legal", plan["legal"])
                future_operations = executor.submit(analyze_with_role, "Operations", plan["operations"])

                compliance_report, compliance_clauses = future_compliance.result()
                finance_report, finance_clauses = future_finance.result()
                legal_report, legal_clauses = future_legal.result()
                operations_report, operations_clauses = future_operations.result()

            # Aggregation
            final_report = generate_final_report(
                compliance_report,
                finance_report,
                legal_report,
                operations_report
            )

            # Risk Score
            overall_risk = risk_score(text)

        # Display Results

        st.subheader("Compliance Analysis")
        st.write(compliance_report)

        with st.expander("🔎 Relevant Clauses Used"):
            for clause in compliance_clauses:
                st.markdown(f"- {clause}")

        st.subheader("Finance Analysis")
        st.write(finance_report)

        with st.expander("🔎 Relevant Clauses Used"):
            for clause in compliance_clauses:
                st.markdown(f"- {clause}")

        st.subheader("Legal Analysis")
        st.write(legal_report)

        with st.expander("🔎 Relevant Clauses Used"):
            for clause in compliance_clauses:
                st.markdown(f"- {clause}")

        st.subheader("Operations Analysis")
        st.write(operations_report)

        with st.expander("🔎 Relevant Clauses Used"):
            for clause in compliance_clauses:
                st.markdown(f"- {clause}")
                
        st.subheader("Executive Summary")
        st.write(final_report)

        st.subheader("Overall Risk Score")
        st.write(f"{overall_risk}/100")

        ai_risk = ai_risk_assessment(text)

        st.subheader("AI-Based Risk Assessment")
        st.write(ai_risk)

        # 🔥 Risk Level Indicator
        if overall_risk < 40:
            st.success("Low Risk 🟢")
        elif overall_risk < 70:
            st.warning("Moderate Risk 🟡")
        else:
            st.error("High Risk 🔴")