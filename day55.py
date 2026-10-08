"""
AI-Powered Spam Classifier Prediction Engine (Text Classification)
================================================================
Phase: Mini Project

Description:
Building on our text preprocessing pipeline, this script trains an actual machine learning 
model to automatically classify incoming messages as spam or legitimate (ham). It converts 
raw text into TF-IDF numerical vectors, trains a Multinomial Naive Bayes classifier, 
evaluates performance metrics, and makes real-time predictions on custom messages.

Real-World Impact:
- Automated Moderation: Filtering millions of spam messages and phishing attempts in real-time.
- Fraud Detection: Identifying malicious text alerts and scam notifications.
- Recommendation Systems: Categorizing user intent across chat and support tickets.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Expanded Dataset for Machine Learning Training & Testing
# Format: (message_text, label) -> label: 'ham' (legitimate) or 'spam'
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

class SpamClassificationEngine:
    """
    An end-to-end machine learning wrapper for spam detection using TF-IDF 
    vectorization and Multinomial Naive Bayes classification.
    """
    def __init__(self):
        # Pipeline combines TF-IDF vectorizer and Naive Bayes classifier into a single object
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(stop_words='english', lowercase=True)),
            ('clf', MultinomialNB())
        ])
        self.is_trained = False

    def train(self, data: list[tuple[str, str]]):
        """Trains the model on text-label pairs using an 80/20 train-test split."""
        texts = [item[0] for item in data]
        labels = [item[1] for item in data]
        
        # Split data for rigorous evaluation (80% training, 20% testing)
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=0.25, random_state=42
        )
        
        print(f"[TRAINING] Training model on {len(X_train)} messages...")
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        # Evaluate model accuracy on the test set
        predictions = self.model.predict(X_test)
        acc = accuracy_score(y_test, predictions)
        
        print(f"[EVALUATION] Model Test Accuracy: {acc * 100:.2f}%")
        print("\n--- Detailed Classification Report ---")
        print(classification_report(y_test, predictions, zero_division=0))
        print("---------------------------------------")

    def predict(self, message: str) -> str:
        """Classifies a custom message as 'spam' or 'ham'."""
        if not self.is_trained:
            raise Exception("Model has not been trained yet!")
            
        prediction = self.model.predict([message])[0]
        probabilities = self.model.predict_proba([message])[0]
        confidence = max(probabilities) * 100
        
        return f"{prediction.upper()} (Confidence: {confidence:.1f}%)"


# --- Execution and Testing Suite ---
if __name__ == "__main__":
    print("=== AI SPAM CLASSIFIER PREDICTION ENGINE ===")
    
    # Initialize and train engine
    engine = SpamClassificationEngine()
    engine.train(DATASET)
    
    # Test predictions on custom unseen messages
    print("\n[Testing Custom Messages]")
    test_messages = [
        "Hey boss, can we push the sprint planning meeting to 3 PM?",
        "URGENT! You have won a brand new iPhone. Click here to claim your prize now!",
        "Can you send over the API documentation for the payment gateway?",
        "CONGRATULATIONS! Claim your $500 gift card immediately by texting WIN."
    ]
    
    for msg in test_messages:
        result = engine.predict(msg)
        print(f" - Message : '{msg}'")
        print(f"   Verdict : {result}\n")
