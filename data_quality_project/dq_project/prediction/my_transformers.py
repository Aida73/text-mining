import spacy
import spacy.cli
from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop
import string
import language_tool_python
import unidecode
from sklearn.base import TransformerMixin
import pickle


nlp = spacy.load("fr_core_news_sm")
punctuations = string.punctuation


tool = language_tool_python.LanguageTool(
    'fr', config={'cacheSize': 2000, 'pipelineCaching': True})


def clean_txt(word):
    cleaned = word.translate(
        {ord(c): " " for c in string.punctuation})
    return cleaned


def clean_txt_2(text):
    nlp.get_pipe("lemmatizer").lookups.get_table(
        "lemma_rules")["verb"] += [['e', 'er']]
    return " ".join([t.lemma_ for t in nlp(text)])


def getCorrectWordTool(word):
    text = tool.correct(clean_txt(word))
    final_text = clean_txt_2(text)
    return unidecode.unidecode(final_text)


def spacy_tokenizer(sentence):
    mytokens = [t.lemma_ for t in nlp(sentence)]
    # Removing stop words
    mytokens = [
        word for word in mytokens if word not in fr_stop and word not in punctuations]
    return mytokens

# Basic function to clean the text


def clean_text(text):
    """Removing spaces and converting the text into lowercase"""
    return text.strip().lower()


# Custom transformer using spaCy
class predictors(TransformerMixin):
    def transform(self, X, **transform_params):
        """Override the transform method to clean text"""
        return [getCorrectWordTool(clean_text(text)) for text in X]

    def fit(self, X, y=None, **fit_params):
        return self

    def get_params(self, deep=True):
        return {}


def load_model(text):
    model = pickle.load(open('dq_app/profession_model.sav', 'rb'))
    prediction = model.predict([text.lower()])
    return prediction[0]
