import re


def calculate_priority(complaint, category):
    """
    Calculate a transparent priority score for a civic complaint.

    Returns:
        score: integer from 0 to 100
        level: LOW / MEDIUM / HIGH
        reasons: list of explanations
    """

    text = complaint.lower()

    score = 10
    reasons = []

    # 1. Emergency / urgency indicators

    urgent_words = [
        "urgent",
        "emergency",
        "immediately",
        "danger",
        "dangerous",
        "critical",
        "life threatening",
        "life-threatening",
        "accident",
    ]

    urgent_matches = [
        word for word in urgent_words
        if word in text
    ]

    if urgent_matches:
        score += 25
        reasons.append("Urgent or emergency situation mentioned")


    # 2. Essential services

    essential_categories = [
        "Water",
        "Healthcare",
        "Electricity",
        "Sanitation",
    ]

    if category in essential_categories:
        score += 20
        reasons.append("Essential public service affected")


    # 3. Vulnerable population

    vulnerable_words = [
        "child",
        "children",
        "elderly",
        "senior citizen",
        "disabled",
        "disability",
        "pregnant",
        "patient",
        "patients",
    ]

    vulnerable_matches = [
        word for word in vulnerable_words
        if word in text
    ]

    if vulnerable_matches:
        score += 20
        reasons.append("Vulnerable population mentioned")


    # 4. Public safety

    safety_words = [
        "fire",
        "accident",
        "injury",
        "injured",
        "electric shock",
        "open manhole",
        "collapsed",
        "collapse",
        "pothole",
        "unsafe",
        "hazard",
    ]

    safety_matches = [
        word for word in safety_words
        if word in text
    ]

    if safety_matches:
        score += 25
        reasons.append("Potential public safety risk")


    # 5. Duration

    duration_patterns = [
        r"(\d+)\s+days?",
        r"(\d+)\s+weeks?",
        r"(\d+)\s+months?",
    ]

    duration_found = False

    for pattern in duration_patterns:
        match = re.search(pattern, text)

        if match:
            duration_found = True

            number = int(match.group(1))

            if number >= 7:
                score += 15
                reasons.append("Problem has continued for a long duration")

            elif number >= 3:
                score += 20
                reasons.append("Problem has continued for several days")

            elif number >= 1:
                score += 5
                reasons.append("Problem has continued over time")

            break

  
    # Limit score

    score = min(score, 100)


    # Priority level

    if score >= 70:
        level = "HIGH"

    elif score >= 45:
        level = "MEDIUM"

    else:
        level = "LOW"


    # Default reason

    if not reasons:
        reasons.append("No major urgency indicators detected")

    return score, level, reasons



# TEST

if __name__ == "__main__":

    test_complaints = [
        (
            "There has been no water in our area for 4 days "
            "and elderly people are affected",
            "Water"
        ),
        (
            "There is a huge pothole on the main road",
            "Roads"
        ),
        (
            "The street lights are not working near my house",
            "Electricity"
        ),
        (
            "Emergency! There has been an accident and people are injured",
            "Other"
        ),
    ]

    for complaint, category in test_complaints:

        score, level, reasons = calculate_priority(
            complaint,
            category
        )

        print("\n" + "=" * 50)
        print("Complaint:", complaint)
        print("Category:", category)
        print("Priority Score:", score)
        print("Priority Level:", level)

        print("Reasons:")

        for reason in reasons:
            print("-", reason)