# CivicResolve AI
# Complaint Verification Risk Engine

import re
from difflib import SequenceMatcher


def clean_text(text):
    """Normalize complaint text."""

    if not text:
        return ""

    text = str(text).lower().strip()

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text


def text_similarity(text1, text2):
    """Calculate similarity between two complaints."""

    text1 = clean_text(text1)
    text2 = clean_text(text2)

    if not text1 or not text2:
        return 0.0

    return SequenceMatcher(None, text1, text2).ratio()


def check_duplicate(complaint, previous_complaints):
    """
    Check whether a complaint is very similar
    to an existing complaint.
    """

    complaint = clean_text(complaint)

    highest_similarity = 0
    matched_complaint = None

    for previous in previous_complaints:

        similarity = text_similarity(
            complaint,
            previous
        )

        if similarity > highest_similarity:
            highest_similarity = similarity
            matched_complaint = previous

    # 85% or above = strong duplicate signal
    if highest_similarity >= 0.85:

        return {
            "duplicate": True,
            "similarity": highest_similarity,
            "matched_complaint": matched_complaint
        }

    return {
        "duplicate": False,
        "similarity": highest_similarity,
        "matched_complaint": matched_complaint
    }


def check_complaint_quality(complaint):
    """
    Check whether the complaint contains enough
    information for verification.
    """

    complaint = clean_text(complaint)

    signals = []

    # Very short complaint
    if len(complaint) < 20:
        signals.append(
            "Complaint contains very limited information"
        )

    # Extremely repetitive characters/words
    words = complaint.split()

    if len(words) >= 5:

        unique_words = set(words)

        repetition_ratio = len(unique_words) / len(words)

        if repetition_ratio < 0.4:

            signals.append(
                "Complaint contains unusually repetitive text"
            )

    # Missing useful contextual information
    location_words = [
        "area",
        "road",
        "street",
        "near",
        "location",
        "village",
        "ward",
        "colony",
        "school",
        "hospital",
        "market"
    ]

    has_location_context = any(
        word in complaint
        for word in location_words
    )

    if not has_location_context:

        signals.append(
            "Location or affected-area information is unclear"
        )

    return signals


def check_excessive_urgency(complaint):
    """
    Detect repeated emergency/urgent language.

    This is only a verification signal.
    It does NOT mean the complaint is false.
    """

    complaint = clean_text(complaint)

    urgent_words = [
        "urgent",
        "emergency",
        "immediately",
        "asap",
        "critical",
        "danger",
        "dangerous"
    ]

    count = 0

    for word in urgent_words:

        if word in complaint:
            count += 1

    if count >= 2:

        return True

    return False


def calculate_verification_risk(
    complaint,
    previous_complaints=None
):
    """
    Calculate verification risk for a complaint.

    Returns:
        risk level
        score
        signals
        recommendation
    """

    if previous_complaints is None:
        previous_complaints = []

    complaint = clean_text(complaint)

    score = 0
    signals = []


    # 1. Complaint quality

    quality_signals = check_complaint_quality(
        complaint
    )

    if quality_signals:

        score += len(quality_signals) * 10

        signals.extend(
            quality_signals
        )


    # 2. Duplicate detection

    duplicate_result = check_duplicate(
        complaint,
        previous_complaints
    )

    if duplicate_result["duplicate"]:

        score += 40

        signals.append(
            "Highly similar complaint already exists"
        )


    # 3. Excessive urgency language

    if check_excessive_urgency(complaint):

        score += 10

        signals.append(
            "Multiple urgent/emergency terms detected"
        )


    # Limit score

    score = min(score, 100)


    # Risk classification

    if score >= 50:

        risk_level = "HIGH"

        recommendation = (
            "Manual verification recommended "
            "before escalation"
        )

    elif score >= 25:

        risk_level = "MEDIUM"

        recommendation = (
            "Request additional information "
            "or supporting evidence"
        )

    else:

        risk_level = "LOW"

        recommendation = (
            "Complaint can proceed with "
            "standard verification"
        )

    return {
        "verification_score": score,
        "risk_level": risk_level,
        "signals": signals,
        "recommendation": recommendation,
        "duplicate_similarity": round(
            duplicate_result["similarity"] * 100,
            2
        )
    }



# TEST

if __name__ == "__main__":

    previous_complaints = [

        "There is a huge pothole on the main road",

        "Garbage has not been collected in our area",

        "Street lights are not working near the market",

        "There has been no water supply in our area"
    ]

    test_complaints = [

        "There is a huge pothole on the main road",

        "No water in our area for four days and elderly people are affected",

        "urgent urgent emergency problem",

        "Please help",

        "The street lights are not working near our house"
    ]

    for complaint in test_complaints:

        result = calculate_verification_risk(
            complaint,
            previous_complaints
        )

        print("\n" + "=" * 60)

        print("COMPLAINT:")
        print(complaint)

        print("\nVERIFICATION SCORE:")
        print(result["verification_score"])

        print("\nVERIFICATION RISK:")
        print(result["risk_level"])

        print("\nDUPLICATE SIMILARITY:")
        print(
            str(result["duplicate_similarity"]) + "%"
        )

        print("\nSIGNALS:")

        if result["signals"]:

            for signal in result["signals"]:
                print("-", signal)

        else:

            print("- No major verification concerns")

        print("\nRECOMMENDATION:")
        print(result["recommendation"])