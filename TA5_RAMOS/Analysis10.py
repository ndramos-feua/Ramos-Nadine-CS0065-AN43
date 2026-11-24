from textblob import TextBlob
 
positive_count = 0
neutral_count = 0
negative_count = 0
 
for i in range(10):
    print(f"\\nSentence {i + 1}")
    sentence = input("Enter a sentence: ")
    s = TextBlob(sentence)
    p = s.sentiment.polarity
 
    if p < 0:
        print("Sentiment: Negative")
        negative_count += 1
    elif p == 0:
        print("Sentiment: Neutral")
        neutral_count += 1
    else:
        print("Sentiment: Positive")
        positive_count += 1
 
    print("Polarity:", p)
 
print("\\n========== SENTIMENT SUMMARY ==========")
print("Total Positive Sentences:", positive_count)
print("Total Neutral Sentences:", neutral_count)
print("Total Negative Sentences:", negative_count)
print("Total Sentences Analyzed:",
      positive_count + neutral_count + negative_count)
