"""
AI-Powered Spam Detection Engine: Data Preprocessing & Analysis
==============================================================
Phase: Mini Project

Description:
A messaging company is losing millions due to spam messages bypassing filters. 
This script builds the data preprocessing pipeline for an AI-powered spam detection 
engine, cleaning raw message data, removing noise (punctuation and stopwords), and 
exploring linguistic patterns between spam and legitimate (ham) messages.

Real-World Impact:
- Cybersecurity: Protecting users from phishing, malware links, and social engineering.
- Platform Moderation: Keeping email inboxes and social media chats clean and secure.
"""

import re
import string
from collections import Counter

# Built-in sample dataset of SMS messages for standalone execution
RAW_SMS_DATASET = [
    ("ham", "Hey, are we still meeting for lunch today at 12:30 PM? Let me know."),
    ("spam", "WINNER! As a valued network customer you have been selected to win a 1000 cash prize. Call now 09061701461!"),
    ("ham", "Don't forget to submit the quarterly engineering report by Friday morning."),
    ("spam", "URGENT! Your mobile account has been suspended. Click https://fake-secure-link.com to verify your details immediately."),
    ("ham", "Can you pick up some milk and eggs on your way home from work?"),
    ("spam", "FREE ringtone! Text WIN to 8007 to download top chart hits straight to your phone right now!"),
    ("ham", "The code review for the database migration looks solid. Merging branches now."),
    ("spam", "CONGRATULATIONS! You've won a free vacation package to Hawaii. Reply YES to claim your ticket."),
    ("ham", "Let's schedule a sync call tomorrow to discuss the system architecture roadmap."),
    ("spam", "Claim your exclusive reward! Earn $500 daily working from home. Reply STOP to opt out.")
]

# Standard English stopwords to filter out low-value noise words
STOPWORDS = {
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", 
    "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", 
    "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", 
    "theirs", "themselves", "what", "which", "who", "whom", "this", "that", 
    "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", 
    "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", 
    "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", 
    "at", "by", "for", "with", "about", "against", "between", "into", "through", 
    "during", "before", "after", "above", "below", "to", "from", "up", "down", 
    "in", "out", "on", "off", "over", "under", "again", "further", "then", 
    "once", "here", "there", "when", "where", "why", "how", "all", "each", 
    "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", 
    "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", 
    "don", "should", "now"
}


def preprocess_text(text: str) -> list[str]:
    """
    Cleans and tokenizes raw message text:
    1. Converts text to lowercase.
    2. Strips punctuation.
    3. Tokenizes into words.
    4. Removes English stopwords.
    """
    # Convert to lowercase
    text_lower = text.lower()
    
    # Remove punctuation
    translator = str.maketrans('', '', string.punctuation)
    clean_text = text_lower.translate(translator)
    
    # Tokenize by whitespace
    tokens = clean_text.split()
    
    # Filter out stopwords
    filtered_tokens = [word for word in tokens if word not in STOPWORDS]
    
    return filtered_tokens


def explore_spam_patterns(dataset: list[tuple[str, str]]):
    """
    Analyzes and compares patterns between spam and ham messages:
    - Average character length
    - Most frequent indicator keywords
    """
    print("\n==================================================")
    print(" EXPLORATORY DATA ANALYSIS: SPAM VS. HAM PATTERNS")
    print("==================================================")
    
    ham_lengths = []
    spam_lengths = []
    ham_tokens = []
    spam_tokens = []
    
