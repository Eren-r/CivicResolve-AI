import streamlit as st
import joblib
import sys
import os


# PATH CONFIGURATION


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SRC_DIR = os.path.join(BASE_DIR, "src")
MODEL_PATH = os.path.join(BASE_DIR, "models", "category_model.pkl")
DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "complaints.csv")

# Allow imports from src/
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)


# IMPORT OUR ENGINES

from department import recommend_department
from resolution import recommend_resolution
from verification import calculate_verification_risk
from priority import calculate_priority


# LOAD ML MODEL

@st.cache_resource
def load_model():

    with open(MODEL_PATH, "rb") as file:
        model = joblib.load(MODEL_PATH)

    return model



# LOAD PREVIOUS COMPLAINTS

def load_previous_complaints():

    complaints = []

    if not os.path.exists(DATA_PATH):
        return complaints

    try:

        import pandas as pd

        df = pd.read_csv(DATA_PATH)

        # Try to find complaint/text column
        possible_columns = [
            "complaint",
            "Complaint",
            "text",
            "Text",
            "description",
            "Description"
        ]

        complaint_column = None

        for column in possible_columns:

            if column in df.columns:
                complaint_column = column
                break

        if complaint_column:

            complaints = (
                df[complaint_column]
                .dropna()
                .astype(str)
                .tolist()
            )

    except Exception:
        pass

    return complaints


# CATEGORY PREDICTION

def predict_category(model, complaint):

    prediction = model.predict([complaint])[0]

    confidence = None

    # If model supports probability
    if hasattr(model, "predict_proba"):

        probabilities = model.predict_proba(
            [complaint]
        )[0]

        confidence = max(probabilities) * 100

    return str(prediction), confidence


# PAGE CONFIG

st.set_page_config(
    page_title="CivicResolve AI",
    page_icon="🏛️",
    layout="wide"
)



# HEADER

st.title("🏛️ CivicResolve AI")

st.subheader(
    "AI-Powered Public Grievance Analysis & "
    "Resolution Recommendation Platform"
)

st.markdown(
    """
CivicResolve AI transforms citizen complaints into
**actionable civic intelligence** using AI-based
classification, priority analysis, verification signals,
department routing and resolution recommendations.
"""
)

st.divider()


# SIDEBAR

with st.sidebar:

    st.header("⚙️ System")

    st.success("AI Model Loaded")

    st.markdown("### Pipeline")

    st.write("1️⃣ Complaint Classification")
    st.write("2️⃣ Priority Assessment")
    st.write("3️⃣ Verification Analysis")
    st.write("4️⃣ Department Recommendation")
    st.write("5️⃣ Resolution Recommendation")


# LOAD MODEL

try:

    model = load_model()

except Exception as e:

    st.error(
        "Could not load the trained model."
    )

    st.code(str(e))

    st.stop()



# COMPLAINT INPUT

st.header("📝 Submit Citizen Complaint")

complaint = st.text_area(
    "Enter complaint",
    placeholder=(
        "Example: There has been no water in "
        "our area for 4 days and elderly people "
        "are affected."
    ),
    height=150
)


analyze = st.button(
    "🔍 Analyze Complaint",
    type="primary",
    use_container_width=True
)


# ANALYSIS

if analyze:

    if not complaint.strip():

        st.warning(
            "Please enter a complaint first."
        )

        st.stop()


    # CATEGORY

    category, confidence = predict_category(
        model,
        complaint
    )

 
    # PRIORITY

    priority_score, priority_level, priority_reasons = (
        calculate_priority(
            complaint,
            category
        )
    )


    # VERIFICATION

    previous_complaints = load_previous_complaints()

    verification = calculate_verification_risk(
        complaint,
        previous_complaints
    )


    # DEPARTMENT

    department = recommend_department(
        category
    )


    # RESOLUTION

    resolution = recommend_resolution(
        category
    )



    # RESULTS

    st.divider()

    st.header("📊 AI Analysis Result")



    # TOP METRICS

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Category",
            category
        )

    with col2:

        st.metric(
            "Priority",
            priority_level
        )

    with col3:

        st.metric(
            "Priority Score",
            priority_score
        )

    with col4:

        st.metric(
            "Verification Risk",
            verification["risk_level"]
        )


    # CATEGORY CONFIDENCE

    if confidence is not None:

        st.subheader("🤖 AI Classification")

        st.progress(
            min(confidence / 100, 1.0)
        )

        st.write(
            f"Classification confidence: "
            f"**{confidence:.2f}%**"
        )



    # PRIORITY

    st.subheader("🚨 Priority Analysis")

    if priority_level == "HIGH":

        st.error(
            f"HIGH PRIORITY — Score: {priority_score}"
        )

    elif priority_level == "MEDIUM":

        st.warning(
            f"MEDIUM PRIORITY — Score: {priority_score}"
        )

    else:

        st.info(
            f"LOW PRIORITY — Score: {priority_score}"
        )


    if priority_reasons:

        st.write("**Reasons:**")

        for reason in priority_reasons:

            st.write(
                f"• {reason}"
            )



    # VERIFICATION

    st.subheader("🔎 Complaint Verification")

    verification_score = verification[
        "verification_score"
    ]

    st.write(
        f"Verification score: "
        f"**{verification_score}/100**"
    )

    st.write(
        f"Duplicate similarity: "
        f"**{verification['duplicate_similarity']}%**"
    )


    if verification["risk_level"] == "HIGH":

        st.error(
            "⚠️ HIGH VERIFICATION RISK"
        )

    elif verification["risk_level"] == "MEDIUM":

        st.warning(
            "⚠️ ADDITIONAL VERIFICATION RECOMMENDED"
        )

    else:

        st.success(
            "✅ LOW VERIFICATION RISK"
        )


    if verification["signals"]:

        st.write("**Detected signals:**")

        for signal in verification["signals"]:

            st.write(
                f"• {signal}"
            )

    else:

        st.write(
            "No major verification concerns detected."
        )


    st.info(
        "Verification risk is a signal for review, "
        "not a determination that a complaint is false."
    )



    # DEPARTMENT

    st.subheader("🏢 Department Recommendation")

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            "**Department**"
        )

        st.success(
            department["department"]
        )

    with col2:

        st.write(
            "**Responsible Officer**"
        )

        st.info(
            department["officer"]
        )


 
    # IMMEDIATE ACTION

    st.subheader("⚡ Recommended Immediate Actions")

    for action in resolution[
        "immediate_action"
    ]:

        st.write(
            f"• {action}"
        )



    # RESOLUTION

    st.subheader("🛠️ Recommended Resolution")

    st.success(
        resolution["resolution"]
    )



    # FOLLOW UP

    st.subheader("🔄 Follow-up")

    st.write(
        resolution["follow_up"]
    )



    # FINAL DECISION

    st.divider()

    st.header("🎯 Recommended Workflow")

    if verification["risk_level"] == "HIGH":

        st.warning(
            """
            ⚠️ **MANUAL VERIFICATION REQUIRED**

            The complaint contains verification signals.
            Review the complaint before escalation.
            """
        )

    elif priority_level == "HIGH":

        st.error(
            """
            🚨 **PRIORITY ESCALATION**

            Forward the complaint to the recommended
            department for urgent review.
            """
        )

    else:

        st.success(
            """
            ✅ **STANDARD PROCESSING**

            Forward the complaint to the recommended
            department for normal verification and resolution.
            """
        )


st.divider()

st.caption(
    "CivicResolve AI"
)