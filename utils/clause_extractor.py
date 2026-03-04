def extract_clauses(text):
    keywords = [
        "payment", "termination", "liability",
        "confidentiality", "penalty", "governing law"
    ]

    clauses = []
    for line in text.split("\n"):
        for word in keywords:
            if word.lower() in line.lower():
                clauses.append(line)
                break

    return clauses
