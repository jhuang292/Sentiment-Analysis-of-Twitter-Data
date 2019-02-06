import sys

def create_sent_dict(sentiment_file):
    """A function that creates a dictionary which contains terms as keys and their sentiment score as value

        Args:
            sentiment_file (string): The name of a tab-separated file that contains
                                     all terms and scores (e.g., the AFINN file).

        Returns:
            dicitonary: A dictionary with schema d[term] = score
        """
    scores = {}
    
    afinnfile = open(sentiment_file, 'r')
    for line in afinnfile:
        term, score = line.split("\t")
        scores[term] = int(score)
    afinnfile.close()
    
    return scores

def get_tweet_sentiment(tweet, sent_scores):
    """A function that find the sentiment of a tweet and outputs a sentiment score.

            Args:
                tweet (string): A clean tweet
                sent_scores (dictionary): The dictionary output by the method create_sent_dict

            Returns:
                score (numeric): The sentiment score of the tweet
        """
    score = 0

    item_list = tweet.split()
    phase_list = []
    for i in range(len(item_list)):
        phase = ""
        if item_list[i] in sent_scores.keys():
            phase += str(item_list[i]) + " "
            i += 1
        phase = str(phase[:-1])
        phase_list.append(phase)
    for item in phase_list:
        if item in sent_scores.keys():
            score += sent_scores[item]
    
    return score

def term_sentiment(sent_scores, tweets_file):
    """A function that creates a dictionary which contains terms as keys and their sentiment score as value

            Args:
                sent_scores (dictionary): A dictionary with terms and their scores (the output of create_sent_dict)
                tweets_file (string): The name of a txt file that contain the clean tweets
            Returns:
                dicitonary: A dictionary with schema d[new_term] = score
            """
    new_term_sent = {}
    
    tweets = open(tweets_file, 'r')
    for tweet in tweets:
        score = get_tweet_sentiment(tweet, sent_scores)
        
        tweet_list = tweet.split()
        for item in tweet_list:
            if item not in sent_scores.keys():
                if item not in new_term_sent.keys():
                    if score > 0:
                        new_term_sent[item] = 1
                    else:
                        new_term_sent[item] = -1
                else:
                    if score > 0:
                        new_term_sent[item] += 1
                    else:
                        new_term_sent[item] -= 1

    return new_term_sent


def main():
    sentiment_file = sys.argv[1]
    tweets_file = sys.argv[2]

    # Read the AFINN-111 data into a dictionary
    sent_scores = create_sent_dict(sentiment_file)

    # Derive the sentiment of new terms
    new_term_sent = term_sentiment(sent_scores, tweets_file)

    for term in new_term_sent:        
        print(term, new_term_sent[term])


if __name__ == '__main__':
    main()
