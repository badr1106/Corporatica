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

def summarize_text(text, max_length=130, min_length=30):
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']

def extract_keywords(text, num_keywords=10):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
    word_freq = Counter(words)
    most_common = word_freq.most_common(num_keywords)
    return [word for word, freq in most_common]

def analyze_sentiment(text):
    result = sentiment_analyzer(text)
    return result[0]