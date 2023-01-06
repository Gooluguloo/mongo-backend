from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

ps = PorterStemmer()

def process_context(input):
    context = ps.stem(input)
    result = word_tokenize(context)
    return result
