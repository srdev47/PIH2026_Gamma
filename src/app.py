import re
import joblib
import streamlit as st

MODEL_PATH = "models/model.joblib"

# -------------------------
# Red flag rules
# -------------------------
RED_FLAGS = [
    (
        r"\bwhatsapp\b|\btelegram\b|\bsignal\b",
        "Asked to move to WhatsApp/Telegram (common scam pattern).",
    ),
    (
        r"\bpay\b.*\bfee\b|\bregistration fee\b|\btraining fee\b|\bsecurity deposit\b|\bdeposit\b",
        "Mentions paying a fee/deposit (real jobs rarely require upfront payment).",
    ),
    (
        r"\bgift card\b|\bcrypto\b|\bbitcoin\b|\busdt\b",
        "Mentions gift cards/crypto payment (high-risk scam indicator).",
    ),
    (
        r"\burgent\b|\bimmediate join\b|\bhire today\b|\bwithin 24 hours\b",
        "Creates urgency/pressure to act quickly.",
    ),
    (
        r"\bno interview\b|\bdirect selection\b|\b100%\b|\bguaranteed\b",
        "Unrealistic hiring promise (no interview/guarantee).",
    ),
    (
        r"\baadhaar\b|\bpan\b|\bpassport\b|\bssn\b|\baccount number\b|\bbank\b|\botp\b",
        "Asks for sensitive ID/banking details too early.",
    ),
]

VERIFY_STEPS = [
    "Check the company’s official website and email domain.",
    "Search the same job on the company’s official careers page.",
    "Verify recruiter/company on LinkedIn.",
    "Never pay any hiring/training/verification fees.",
    "Ask for official offer letter after proper interview process.",
]


def detect_red_flags(text: str):
    hits = []
    for pattern, reason in RED_FLAGS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            hits.append(reason)

    if len(text.strip()) < 120:
        hits.append("Very short/low-detail job description.")

    # remove duplicates
    return list(dict.fromkeys(hits))


# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="Fake Job Detector", page_icon="🕵️")

st.title("🕵️ Fake Job Detector")
st.write(
    "Paste a job description below. The system predicts whether it looks FAKE or REAL."
)


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


model = load_model()

job_desc = st.text_area("Job Description", height=250)

col1, col2 = st.columns(2)
with col1:
    predict_btn = st.button("Predict")
with col2:
    clear_btn = st.button("Clear")

if clear_btn:
    st.experimental_rerun()

if predict_btn:
    if not job_desc.strip():
        st.warning("Please enter a job description.")
        st.stop()

    proba = model.predict_proba([job_desc])[0]
    pred = int(model.predict([job_desc])[0])  # 0=real, 1=fake

    fake_prob = float(proba[1])
    real_prob = float(proba[0])

    st.subheader("Result")

    if pred == 1:
        st.error(f"Likely FAKE (confidence: {fake_prob:.2%})")
    else:
        st.success(f"Likely REAL (confidence: {real_prob:.2%})")

    st.caption(
        "Treat this as a risk signal, not a guarantee. Always verify independently."
    )

    # Show practical pointers
    st.subheader("Why it might be risky")
    flags = detect_red_flags(job_desc)

    if flags:
        for f in flags:
            st.write(f"- {f}")
    else:
        st.write("- No obvious scam keywords detected.")

    st.subheader("What you should verify next")
    for step in VERIFY_STEPS:
        st.write(f"- {step}")
