import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from transformers import pipeline
from collections import Counter
import string

nltk.download('punkt')
nltk.download('stopwords')


summarizer = pipeline("summarization")
sentiment_analyzer = pipeline("sentiment-analysis")
classifier = pipeline("zero-shot-classification")

def search_text(text, query):
    words = word_tokenize(text)
    query_words = word_tokenize(query)
    results = [word for word in words if word in query_words]
    return results

def categorize_text(text, categories):
    result = classifier(text, candidate_labels=categories)
    return result

def custom_query(text, query):
    words = word_tokenize(text)
    query_words = word_tokenize(query)
    results = [word for word in words if word in query_words]
    return results