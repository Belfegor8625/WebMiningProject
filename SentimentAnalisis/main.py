import operator

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import SentimentAnalisis.prep_data as p

nltk.download('vader_lexicon')

sid = SentimentIntensityAnalyzer()


def sentiment_data_collector(xml_name):
    dictionary = {'neg': 0, 'pos': 0, 'neu': 0, 'compound': 0}
    for sentence in p.parse_xml_for_comments(xml_name):
        ss = sid.polarity_scores(sentence)
        # for k in ss:
        # print('{0}: {1}, '.format(k, ss[k]), end='')
        # print()
        dictionary['neg'] += ss['neg']
        dictionary['pos'] += ss['pos']
        # dictionary['neu'] += ss['neu']
        # dictionary['compound'] += ss['compound']
    main_sentiment_in_data(dictionary, xml_name)


def main_sentiment_in_data(stats, xml_name):
    print('For: ' + xml_name)
    print(stats)
    print('Pos or neg? Answear: ' + max(stats.items(), key=operator.itemgetter(1))[0])


#autotagger - treningowe z datadamp

sentiment_data_collector('Comments beer.xml')
sentiment_data_collector('Comments crypto.xml')
sentiment_data_collector('Comments android.xml')
