import gensim
from gensim.matutils import softcossim
from gensim import corpora
import gensim.downloader as api
import csv
import numpy as np


fast_text_model = api.load('fasttext-wiki-news-subwords-300')


time_spent = {}
documents = [
    "The meditation habitat is a close community ready to help you become more mindful. Here you can find motivation to maintain your meditation habits and some experienced individuals that can guide you.",
    "The tennis habitat is all about improvement, regardless of your level of experience. We value hard work and a willingness to help, so try to be as active as possible.",
    "Have you ever struggled to maintain focus on your schoolwork? The school habitat is just for you. We can help you stay dedicated to your academic career and achieve success."
]

# read the time_spent file to find the amount of time that each user has spent on each habitat
with open("time_spent.csv") as time:
    reader = csv.reader(time, delimiter=",")
    for row in reader:
        if(len(row) == 3):
            values = [int(row[0]), int(row[1]), int(row[2])]
            if not values[0] in time_spent.keys():
                time_spent[values[0]] = {}
            if not values[1] in time_spent[values[0]].keys():
                time_spent[values[0]][values[1]] = 0
            time_spent[values[0]][values[1]] += values[2]


# simple preprocessing
def preprocess(words):
    common_words = ["habitat", "stay", "just", "the", "is", "of", "and", "for", "anything", "it", "a", "an", "in", "if", "that", "to", "here", "find", "your", "you", "more", "become", "some", "individuals", "can", "all", "about", "regardless", "we", "so", "be", "as", "ever"]
    punctuation = [".", "!", "?", ",", ";", ":"]

    output = []

    for i in range(len(words)):
        initial_word = words[i]
        if words[i][len(words[i])-1] in punctuation:
            initial_word = words[i][:-1]
        if not initial_word.lower() in common_words:
            output.append(initial_word)
    
    return output


dictionary = corpora.Dictionary([preprocess(doc) for doc in documents])
similarity_matrix = fast_text_model.similarity_matrix(dictionary, tfidf=None, threshold=0.0, exponent=2.0, nonzero_limit=100)


first_sentence = dictionary.doc2bow(preprocess(documents[0]))
second_sentence = dictionary.doc2bow(preprocess(documents[1]))
third_sentence = dictionary.doc2bow(preprocess(documents[2]))


print(softcossim(first_sentence, second_sentence, similarity_matrix))
print(softcossim(first_sentence, third_sentence, similarity_matrix))
print(softcossim(second_sentence, third_sentence, similarity_matrix))
print(softcossim(third_sentence, second_sentence, similarity_matrix))

