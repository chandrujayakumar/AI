from groq import Groq

client = Groq(
    api_key="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"
)

def summarize_clauses(clauses):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are a professional legal contract analysis assistant."
            },
            {
                "role": "user",
                "content": f"""
Analyze the following contract clauses and provide:
1. Key risks
2. Important obligations
3. Clear summary

Clauses:
{clauses}
"""
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content