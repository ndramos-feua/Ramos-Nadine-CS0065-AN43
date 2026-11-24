import nltk
import re
from nltk.corpus import opinion_lexicon

# Download the word dataset
nltk.download("opinion_lexicon", quiet=True)

# Load positive and negative words
happy_words = set(opinion_lexicon.positive())
sad_words = set(opinion_lexicon.negative())

def number_happy(sentence):
    words = re.findall(r"[a-z]+", sentence.lower())
    return sum(1 for word in words if word in happy_words)

def number_sad(sentence):
    words = re.findall(r"[a-z]+", sentence.lower())
    return sum(1 for word in words if word in sad_words)

# Get user input
sentence = input("Enter a sentence: ")

happy = number_happy(sentence)
sad = number_sad(sentence)

print("\n========== SENTIMENT ANALYSIS ==========")
print("Happy Words:", happy)
print("Sad Words:", sad)

if happy > sad:
    print("Tone: Happy")
elif sad > happy:
    print("Tone: Sad")
else:
    print("Tone: Neutral")