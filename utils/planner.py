def extract_keywords(text, keywords):
    lines = text.split("\n")
    matched_lines = []

    for line in lines:
        for word in keywords:
            if word.lower() in line.lower():
                matched_lines.append(line)
                break

    return "\n".join(matched_lines)


def plan_agents(text):

    def safe_extract(keywords):
        extracted = extract_keywords(text, keywords)
        return extracted if extracted.strip() else text[:1000]

    return {
        "compliance": safe_extract(["law", "regulation", "governing"]),
        "finance": safe_extract(["payment", "penalty", "invoice"]),
        "legal": safe_extract(["liability", "termination"]),
        "operations": safe_extract(["service", "delivery"])
    }

def risk_score(text):

    risk_keywords = ["penalty", "liability", "termination", "breach"]

    score = 0
    for word in risk_keywords:
        score += text.lower().count(word)

    normalized = min(score * 5, 100)

    return normalized