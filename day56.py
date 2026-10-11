"""
AI Spam Detector Web Application (Streamlit Deployment)
======================================================
Phase: Mini Project Deployment

Description:
Transforms our machine learning text classification experiment into a fully deployed, 
interactive web application. Users can input custom messages in real-time, instantly 
receive spam vs. legitimate (ham) classifications, and view confidence scores.

Real-World Impact:
- Productization: Bridging the gap between offline data science experiments and user-facing tools.
- Enterprise Moderation: Providing internal safety teams or customer portals with instant classification tools.
"""

import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ==========================================
# 1. MODEL TRAINING & CACHING
# ==========================================
DATASET = [
    ("Hey, are we still meeting for lunch today at 12:30 PM? Let me know.", "ham"),
    ("WINNER! As a valued network customer you have been selected to win a 1000 cash prize. Call now 09061701461!", "spam"),
    ("Don't forget to submit the quarterly engineering report by Friday morning.", "ham"),
    ("URGENT! Your mobile account has been suspended. Click https://fake-secure-link.com to verify your details immediately.", "spam"),
    ("Can you pick up some milk and eggs on your way home from work?", "ham"),
    ("FREE ringtone! Text WIN to 8007 to download top chart hits straight to your phone right now!", "spam"),
    ("The code review for the database migration looks solid. Merging branches now.", "ham"),
    ("CONGRATULATIONS! You've won a free vacation package to Hawaii. Reply YES to claim your ticket.", "spam"),
    ("Let's schedule a sync call tomorrow to discuss the system architecture roadmap.", "ham"),
    ("Claim your exclusive reward! Earn $500 daily working from home. Reply STOP to opt out.", "spam"),
    ("Hi Mom, I'll be arriving home around 6 PM. Please save some dinner for me.", "ham"),
    ("ALERT: Unauthorized login attempt detected on your bank account. Reset your password here: http://bit.ly/scam-link", "spam"),
    ("Please review the pull request I sent over for the authentication service.", "ham"),
    ("EXCLUSIVE DEAL: Get 90% off designer watches today only! Click here to buy now.", "spam"),
    ("Are we still on for our gym session this evening?", "ham"),
    ("URGENT: Your parcel delivery failed. Update your delivery address via this link immediately.", "spam")
]

@st.cache_resource
def load_trained_model():
    """Trains and caches the spam classification pipeline for fast UI responses."""
    texts = [item[0] for item in DATASET]
    labels = [item[1] for item in DATASET]
    
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42
    )
    
    model = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english', lowercase=True)),
        ('clf', MultinomialNB())
    ])
    
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    
    return model, accuracy

model, model_accuracy = load_trained_model()

# ==========================================
# 2. STREAMLIT USER INTERFACE DESIGN
# ==========================================
st.set_page_config(
    page_title="AI Spam Guard",
    page_icon="🛡️",
    layout="centered"
)

# Sidebar Information
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/security-checked.png", width=100)
    st.title("System Specs")
    st.info("Powered by TF-IDF Vectorization & Multinomial Naive Bayes.")
    st.metric(label="Model Accuracy", value=f"{model_accuracy * 100:.1f}%")
    st.markdown("---")
    st.markdown("**Phase:** Mini Project Deployment")
    st.markdown("**Author:** ABTalks 60 Days Challenge")

# Main Header
st.title("🛡️ AI Spam Guard: Enterprise Message Classifier")
st.markdown("Detect phishing links, scam alerts, and junk messages instantly using machine learning.")

st.markdown("---")

# User Input Section
st.subheader("✍️ Test a Message")
user_input = st.text_area(
    "Enter SMS or email text below:",
    placeholder="e.g., URGENT! You've won a $1,000 gift card. Click here...",
    height=120
)

col1, col2 = st.columns([1, 4])

with col1:
    analyze_btn = st.button("Analyze", type="primary")

if analyze_btn:
    if not user_input.strip():
        st.warning("⚠️ Please enter a message to analyze.")
    else:
        # Make prediction
        prediction = model.predict([user_input])[0]
        probabilities = model.predict_proba([user_input])[0]
        classes = model.classes_
        
        # Get confidence score for predicted class
        class_idx = list(classes).index(prediction)
        confidence = probabilities[class_idx] * 100
        
        st.markdown("### 📊 Analysis Results")
        
        if prediction == "spam":
            st.error(f"🚨 **Verdict: SPAM / MALICIOUS** (Confidence: {confidence:.1f}%)")
            st.markdown("> **Warning:** This message contains patterns typical of phishing, scams, or unsolicited junk.")
        else:
            st.success(f"✅ **Verdict: LEGITIMATE (HAM)** (Confidence: {confidence:.1f}%)")
            st.markdown("> **Safe:** This message appears to be normal communication.")

# Sample Quick-Test Buttons
st.markdown("---")
st.subheader("⚡ Quick-Test Samples")
sample_col1, sample_col2 = st.columns(2)

with sample_col1:
    if st.button("Test Legitimate Sample"):
        st.info("Testing: 'Hey, are we still meeting for lunch today?'")
        # Pre-fill behavior simulation via rerun or display
        res = model.predict(["Hey, are we still meeting for lunch today?"])[0]
        st.success(f"Result: {res.upper()}")

with sample_col2:
    if st.button("Test Spam Sample"):
        st.warning("Testing: 'WINNER! You won a cash prize. Call now!'")
        res = model.predict(["WINNER! You won a cash prize. Call now!"])[0]
        st.error(f"Result: {res.upper()}")


# ==========================================
# 3. PROJECT DOCUMENTATION & DEPLOYMENT GUIDE
# ==========================================
"""
--- README DOCUMENTATION & DEPLOYMENT GUIDE ---
1. Prerequisites:
   Install required packages locally:
   `pip install streamlit scikit-learn`

2. Running the App Locally:
   Execute the following command in your terminal:
   `streamlit run app.py`

3. Cloud Deployment:
   - Push this repository to GitHub.
   - Go to Streamlit Community Cloud (share.streamlit.io).
   - Link your repo, select `app.py` as the main file path, and click Deploy!
"""

# ==========================================
# 4. LINKEDIN REFLECTION
# ==========================================
"""
--- LINKEDIN REFLECTION ---
Post Title: From Python Script to Live Web App: Deploying an AI Spam Detector 🚀🌐

Building a machine learning model in a Jupyter notebook is only half the battle. The true 
magic happens when you bridge the gap between offline code and user-facing products! 
Today, as part of the ABTalks 60 Days Challenge, I deployed our AI Spam Detection Engine 
into a fully interactive web application using Streamlit.

Key engineering takeaways from today's deployment:
1. Productization: Wrapping a scikit-learn pipeline into a clean, responsive UI with real-time inference.
2. Performance Optimization: Leveraging `@st.cache_resource` to ensure the model trains instantly on startup without lagging user interactions.
3. User Experience: Providing clear visual feedback, confidence scores, and quick-test samples for security evaluation.

From raw data cleaning to a live deployed app—software engineering is all about delivering end-to-end value!

#SoftwareEngineering #MachineLearning #Streamlit #Python #Deployment #BuildInPublic #CodingJourney
"""
