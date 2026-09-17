import streamlit as st
import joblib
import sys
import os


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "category_model.pkl"
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "complaints.csv"
)

if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)


# ============================================================
# IMPORT PROJECT MODULES
# ============================================================

from department import recommend_department
from resolution import recommend_resolution
from verification import calculate_verification_risk
from priority import calculate_priority


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CivicResolve AI",
    page_icon="🏛️",
    layout="wide"
)

# ============================================================
# SESSION COMPLAINT HISTORY
# ============================================================

if "submitted_complaints" not in st.session_state:
    st.session_state.submitted_complaints = []


# ============================================================
# CUSTOM CSS
# DARK THEME SAFE
# ============================================================

st.markdown(
    """
<style>

/* ============================================================
   MAIN PAGE
   ============================================================ */

.main {
    padding-top: 1rem;
}


/* ============================================================
   HEADER
   ============================================================ */

.civic-header {
    padding: 28px;
    border-radius: 16px;
    margin-bottom: 20px;

    background: linear-gradient(
        135deg,
        #172033,
        #202938
    );

    border: 1px solid #3b4658;
}

.civic-title {
    color: #ffffff;
    font-size: 38px;
    font-weight: 700;
    line-height: 1.2;
}

.civic-subtitle {
    color: #d7dee9;
    font-size: 18px;
    margin-top: 8px;
}


/* ============================================================
   CONFIDENCE CARD
   ============================================================ */

.confidence-card {
    padding: 22px;
    border-radius: 14px;

    background: #111827;

    border: 1px solid #4b5563;

    margin-top: 10px;
    margin-bottom: 12px;
}

.confidence-label {
    color: #d1d5db;
    font-size: 14px;
    font-weight: 600;
}

.confidence-category {
    color: #ffffff;
    font-size: 30px;
    font-weight: 700;
    margin-top: 6px;
}


/* ============================================================
   PRIORITY CARD
   ============================================================ */

.priority-card {
    padding: 24px;
    border-radius: 14px;

    background: #111827;

    border: 1px solid #4b5563;

    margin-top: 10px;
    margin-bottom: 15px;
}

.priority-label {
    color: #d1d5db;
    font-size: 14px;
    font-weight: 600;
}

.priority-level {
    color: #ffffff;
    font-size: 30px;
    font-weight: 700;
    margin-top: 6px;
}

.priority-score {
    color: #ffffff;
    font-size: 25px;
    font-weight: 700;
    margin-top: 8px;
}

.priority-score span {
    color: #cbd5e1;
    font-size: 15px;
    font-weight: 400;
}

.priority-bar {
    width: 100%;
    height: 10px;

    border-radius: 10px;

    background-color: #374151;

    margin-top: 14px;

    overflow: hidden;
}

.priority-fill {
    height: 100%;

    border-radius: 10px;

    background-color: #f59e0b;
}

.priority-message {
    color: #e5e7eb;
    margin-top: 13px;
    font-size: 15px;
}


/* ============================================================
   PRIORITY REASONS
   ============================================================ */

.priority-reason {
    color: #e5e7eb;

    padding: 10px 14px;

    margin-bottom: 7px;

    border-radius: 9px;

    background-color: #1f2937;

    border: 1px solid #374151;
}


/* ============================================================
   VERIFICATION CARD
   ============================================================ */

.verification-card {
    padding: 22px;
    border-radius: 14px;

    background: #111827;

    border: 1px solid #4b5563;

    margin-top: 10px;
    margin-bottom: 12px;
}

.verification-label {
    color: #d1d5db;
    font-size: 14px;
    font-weight: 600;
}

.verification-level {
    color: #ffffff;
    font-size: 30px;
    font-weight: 700;
    margin-top: 6px;
}

.verification-score {
    color: #e5e7eb;
    font-size: 16px;
    margin-top: 10px;
}


/* ============================================================
   FOOTER
   ============================================================ */

.civic-footer {
    text-align: center;

    padding: 20px;

    color: #9ca3af;

    font-size: 14px;

    opacity: 0.9;
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
<div class="civic-header">

<div class="civic-title">
🏛️ CivicResolve AI
</div>

<div class="civic-subtitle">
AI-Powered Public Grievance Analysis & Resolution Recommendation Platform
</div>

</div>
""",
    unsafe_allow_html=True
)


st.markdown(
    """
Transform citizen complaints into **actionable civic intelligence**
through AI-based classification, priority analysis, verification
signals, department routing and resolution recommendations.
"""
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ System")

    st.success("AI Model Loaded")

    st.markdown("### Pipeline")

    st.write("1️⃣ Complaint Classification")

    st.write("2️⃣ Priority Assessment")

    st.write("3️⃣ Verification Analysis")

    st.write("4️⃣ Department Recommendation")

    st.write("5️⃣ Resolution Recommendation")


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():

    model = joblib.load(MODEL_PATH)

    return model


# ============================================================
# LOAD PREVIOUS COMPLAINTS
# ============================================================

def load_previous_complaints():

    complaints = []

    if not os.path.exists(DATA_PATH):

        return complaints

    try:

        import pandas as pd

        df = pd.read_csv(DATA_PATH)

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


# ============================================================
# CATEGORY PREDICTION
# ============================================================

def predict_category(model, complaint):

    prediction = model.predict([complaint])[0]

    confidence = None

    if hasattr(model, "predict_proba"):

        probabilities = model.predict_proba(
            [complaint]
        )[0]

        confidence = max(probabilities) * 100

    return str(prediction), confidence


# ============================================================
# MODEL INITIALIZATION
# ============================================================

try:

    model = load_model()

except Exception as e:

    st.error("Could not load the trained model.")

    st.code(str(e))

    st.stop()


# ============================================================
# COMPLAINT INPUT
# ============================================================

st.header("📝 Submit Citizen Complaint")

complaint = st.text_area(
    "Describe the civic issue",

    placeholder=(
        "Example: There has been no water supply in our area "
        "for 4 days and elderly people are affected."
    ),

    height=160,

    help=(
        "Include useful details such as the problem, location, "
        "duration and people affected."
    )
)


analyze = st.button(
    "🔍 Analyze Complaint",
    type="primary",
    use_container_width=True
)


# ============================================================
# ANALYSIS
# ============================================================

if analyze:

    # ========================================================
    # INPUT VALIDATION
    # ========================================================

    if not complaint.strip():

        st.warning(
            "Please enter a complaint first."
        )

        st.stop()


    # ========================================================
    # 1. CLASSIFICATION
    # ========================================================

    category, confidence = predict_category(
        model,
        complaint
    )

    # ========================================================
    # LOW-CONFIDENCE CLASSIFICATION SAFEGUARD
    # ========================================================

    LOW_CONFIDENCE_THRESHOLD = 60

    low_confidence = (
        confidence is not None
        and confidence < LOW_CONFIDENCE_THRESHOLD
    )   

    # ========================================================
    # 2. PRIORITY
    # ========================================================

    priority_score, priority_level, priority_reasons = (
        calculate_priority(
            complaint,
            category
        )
    )


    # ========================================================
    # 3. VERIFICATION
    # ========================================================

    previous_complaints = load_previous_complaints()

    # Include complaints submitted during the current session
    session_complaints = st.session_state.submitted_complaints

    verification_history = (
        previous_complaints
        + session_complaints
    )

    verification = calculate_verification_risk(
        complaint,
        verification_history
    )

    # Store the complaint for future duplicate checks
    if complaint not in st.session_state.submitted_complaints:
        st.session_state.submitted_complaints.append(
            complaint
        )


    # ========================================================
    # 4. DEPARTMENT
    # ========================================================

    department = recommend_department(
        category
    )


    # ========================================================
    # 5. RESOLUTION
    # ========================================================

    resolution = recommend_resolution(
        category
    )


    # ========================================================
    # AI ANALYSIS RESULT
    # ========================================================

    st.divider()

    st.header(
        "📊 AI Analysis Result"
    )

    st.caption(
        "The complaint has been analyzed across classification, "
        "priority, verification and resolution workflows."
    )


    # ========================================================
    # SUMMARY METRICS
    # ========================================================

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


    # ========================================================
    # AI CLASSIFICATION
    # ========================================================

    if confidence is not None:

        st.subheader(
            "🤖 AI Classification"
        )


        if confidence >= 80:

            confidence_status = (
                "High confidence"
            )

            confidence_message = (
                "The model shows strong confidence "
                "in this category."
            )

            confidence_icon = "🟢"


        elif confidence >= LOW_CONFIDENCE_THRESHOLD:

            confidence_status = (
                "Moderate confidence"
            )

            confidence_message = (
                "The model has reasonable confidence, "
                "but review is recommended for important decisions."
            )

            confidence_icon = "🟡"


        else:

            confidence_status = (
                "Low confidence"
            )

            confidence_message = (
                "The model has limited confidence in this "
                "classification. Manual review is recommended "
                "before departmental escalation."
            )

            confidence_icon = "🔴"


        st.markdown(
            f"""
<div class="confidence-card">

<div class="confidence-label">
Predicted Category
</div>

<div class="confidence-category">
{category}
</div>

</div>
""",
            unsafe_allow_html=True
        )


        st.markdown(
            f"**Model Confidence: {confidence:.2f}%**"
        )


        st.progress(
            min(confidence / 100, 1.0)
        )


        st.info(
            f"{confidence_icon} **{confidence_status}** — "
            f"{confidence_message}"
        )

        if low_confidence:

            st.warning(
                "⚠️ **HUMAN REVIEW RECOMMENDED** — "
                "The AI classification confidence is below "
                f"{LOW_CONFIDENCE_THRESHOLD}%. "
                "Verify the complaint category before "
                "departmental escalation."
            )


    # ========================================================
    # PRIORITY ANALYSIS
    # ========================================================

    st.subheader(
        "🚨 Priority Analysis"
    )


    if priority_level == "HIGH":

        priority_icon = "🔴"

        priority_message = (
            "High-priority complaint requiring prompt attention."
        )


    elif priority_level == "MEDIUM":

        priority_icon = "🟡"

        priority_message = (
            "Moderate-priority complaint requiring timely attention."
        )


    else:

        priority_icon = "🟢"

        priority_message = (
            "Low-priority complaint suitable for standard processing."
        )


    st.markdown(
        f"""
<div class="priority-card">

<div class="priority-label">
Priority Level
</div>

<div class="priority-level">
{priority_icon} {priority_level}
</div>

<div class="priority-score">
{priority_score}
<span>/ 100</span>
</div>

<div class="priority-bar">

<div class="priority-fill"
style="width:{priority_score}%">
</div>

</div>

<div class="priority-message">
{priority_message}
</div>

</div>
""",
        unsafe_allow_html=True
    )


    st.markdown(
        "**Why this priority?**"
    )


    for reason in priority_reasons:

        st.markdown(
            f"""
<div class="priority-reason">
✓ {reason}
</div>
""",
            unsafe_allow_html=True
        )


    # ========================================================
    # VERIFICATION
    # ========================================================

    st.subheader(
        "🔎 Complaint Verification"
    )


    verification_score = (
        verification["verification_score"]
    )

    verification_level = (
        verification["risk_level"]
    )

    duplicate_similarity = (
        verification["duplicate_similarity"]
    )


    if verification_level == "HIGH":

        verification_icon = "🔴"

        verification_message = (
            "Manual verification is recommended "
            "before escalation."
        )


    elif verification_level == "MEDIUM":

        verification_icon = "🟡"

        verification_message = (
            "Additional information or evidence "
            "is recommended."
        )


    else:

        verification_icon = "🟢"

        verification_message = (
            "No major verification concerns were detected."
        )


    st.markdown(
        f"""
<div class="verification-card">

<div class="verification-label">
Verification Risk
</div>

<div class="verification-level">
{verification_icon} {verification_level}
</div>

<div class="verification-score">
Verification Score:
<strong>{verification_score}/100</strong>
</div>

</div>
""",
        unsafe_allow_html=True
    )


    st.progress(
        min(
            verification_score / 100,
            1.0
        )
    )


    if verification_level == "HIGH":

        st.error(
            f"⚠️ **HIGH VERIFICATION RISK** — "
            f"{verification_message}"
        )


    elif verification_level == "MEDIUM":

        st.warning(
            f"⚠️ **MEDIUM VERIFICATION RISK** — "
            f"{verification_message}"
        )


    else:

        st.success(
            f"✅ **LOW VERIFICATION RISK** — "
            f"{verification_message}"
        )


    st.write(
        f"**Duplicate similarity:** "
        f"{duplicate_similarity}%"
    )


    if verification["signals"]:

        st.write(
            "**Detected signals:**"
        )

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


    # ========================================================
    # DEPARTMENT RECOMMENDATION
    # ========================================================

    st.subheader(
        "🏢 Department Recommendation"
    )


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


    # ========================================================
    # IMMEDIATE ACTIONS
    # ========================================================

    st.subheader(
        "⚡ Recommended Immediate Actions"
    )


    for action in resolution["immediate_action"]:

        st.write(
            f"• {action}"
        )


    # ========================================================
    # RECOMMENDED RESOLUTION
    # ========================================================

    st.subheader(
        "🛠️ Recommended Resolution"
    )


    st.success(
        resolution["resolution"]
    )


    # ========================================================
    # FOLLOW-UP
    # ========================================================

    st.subheader(
        "🔄 Follow-up"
    )


    st.write(
        resolution["follow_up"]
    )


    # ========================================================
    # CIVICRESOLVE DECISION PIPELINE
    # ========================================================

    st.subheader(
        "🔄 CivicResolve Decision Pipeline"
    )


    pipeline_cols = st.columns(5)


    # --------------------------------------------------------
    # CITIZEN
    # --------------------------------------------------------

    with pipeline_cols[0]:

        st.markdown("### 👤")

        st.markdown(
            "**Citizen**"
        )

        st.caption(
            "Submit complaint"
        )


    # --------------------------------------------------------
    # AI ANALYSIS
    # --------------------------------------------------------

    with pipeline_cols[1]:

        st.markdown("### 🤖")

        st.markdown(
            "**AI Analysis**"
        )

        st.caption(
            "Classify • Prioritize • Verify"
        )


    # --------------------------------------------------------
    # DEPARTMENT
    # --------------------------------------------------------

    with pipeline_cols[2]:

        st.markdown("### 🏢")

        st.markdown(
            "**Department**"
        )

        st.caption(
            "Intelligent routing"
        )


    # --------------------------------------------------------
    # ACTION
    # --------------------------------------------------------

    with pipeline_cols[3]:

        st.markdown("### ⚡")

        st.markdown(
            "**Action**"
        )

        st.caption(
            "Recommended resolution"
        )


    # --------------------------------------------------------
    # FOLLOW-UP
    # --------------------------------------------------------

    with pipeline_cols[4]:

        st.markdown("### 🔄")

        st.markdown(
            "**Follow-up**"
        )

        st.caption(
            "Confirm resolution"
        )


    # ========================================================
    # RECOMMENDED WORKFLOW
    # ========================================================

    st.divider()

    st.header(
        "🎯 Recommended Workflow"
    )


    if verification["risk_level"] == "HIGH":

        st.warning(
        """
⚠️ **MANUAL VERIFICATION REQUIRED**

The complaint contains verification signals.
Review the complaint before escalation.
"""
    )


    elif low_confidence:

        st.warning(
        """
⚠️ **CLASSIFICATION REVIEW REQUIRED**

The AI model has low confidence in the predicted
category. Verify the category before departmental
escalation.
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


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
<div class="civic-footer">

CivicResolve AI · AI-assisted civic grievance intelligence

</div>
""",
    unsafe_allow_html=True
)