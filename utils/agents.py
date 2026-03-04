from groq import Groq

from utils.vector_store import query_relevant_chunks

client = Groq(api_key="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")


def analyze_with_role(role, text):

    relevant_chunks = query_relevant_chunks(role)

    # Remove duplicates while preserving order
    seen = set()
    unique_chunks = []
    for chunk in relevant_chunks:
        if chunk not in seen:
            unique_chunks.append(chunk)
            seen.add(chunk)

    relevant_chunks = unique_chunks

    limited_text = "\n".join(relevant_chunks)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": f"""
    You are a strict {role} contract analyst.

    IMPORTANT RULES:
    - Use ONLY the provided contract clauses.
    - Do NOT assume laws not mentioned.
    - Do NOT reference external jurisdictions.
    - If something is not in the provided text, say:
    "Not specified in the provided contract."
    """
            },
            {
                "role": "user",
                "content": f"""
    Analyze the following retrieved clauses from a {role} perspective.

    Retrieved Clauses:
    {limited_text}
    """
            }
        ],
        temperature=0,
        max_tokens=300
    )

    if response and response.choices:
        analysis = response.choices[0].message.content
    else:
        analysis = "No analysis generated."

    return analysis, relevant_chunks


def generate_final_report(compliance, finance, legal, operations):

    combined = f"""
Compliance Analysis:
{compliance}

Finance Analysis:
{finance}

Legal Analysis:
{legal}

Operations Analysis:
{operations}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a senior legal contract review manager. Provide a contract-specific executive summary."},
            {"role": "user", "content": f"Create a structured executive summary with:\n1. Key Risks\n2. Critical Obligations\n3. Financial Impact\n4. Overall Assessment\n\n{combined}"}
        ],
        temperature=0,
        max_tokens=300
    )

    if response and response.choices:
        return response.choices[0].message.content
    else:
        return "Executive summary could not be generated."

def ai_risk_assessment(text):

    limited_text = text[:1200]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a legal risk assessment expert."},
            {"role": "user", "content": f"""
Evaluate the contract and provide:
1. Overall Risk Level (Low / Moderate / High)
2. Top 3 Risk Factors
3. Brief justification

Contract:
{limited_text}
"""}
        ],
        max_tokens=300
    )

    return response.choices[0].message.content