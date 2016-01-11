import nltk
nltk.download('punkt')

def get_scores(): 
    file = open("AFINN-111.txt")
    scores = {}
    for line in file:
      term, score  = line.split("\t")
      scores[term] = int(score)

    return scores

def tweet_score(tweet):
    scores = get_scores()

    words = nltk.word_tokenize(tweet)
    
    score = 0
    for w in words:
        if w.lower() in scores:
            score += scores[w.lower()]
          
    return score