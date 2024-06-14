import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

def pre_process_text(text):
    
    tokens = word_tokenize(text.lower())

    # remove stop words
    filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]

    
    # Lemmatize text
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]

    
    # Join tokens in processed string
    processed_text = ' '.join(lemmatized_tokens)

    return processed_text


def get_sentiment(text): 

    analyzer = SentimentIntensityAnalyzer()

    scores = analyzer.polarity_scores(text)
    # sentiment = 1 if scores['pos'] > 0 else 0

    return scores['compound']
