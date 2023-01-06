from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

wnl = WordNetLemmatizer()

def process_context(input):
    context = wnl.lemmatize(input)
    result = word_tokenize(context)
    for i in range(len(result)):
        result[i] = result[i].lower()
    return result
