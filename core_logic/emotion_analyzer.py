from textblob import TextBlob

def analyze_emotion(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0.5:
        emotion = "joyful"
    elif polarity > 0.1:
        emotion = "positive"
    elif polarity < -0.5:
        emotion = "angry"
    elif polarity < -0.1:
        emotion = "sad"
    else:
        emotion = "neutral"

    return {
        "label": emotion,
        "score": round(polarity, 2)
    }
