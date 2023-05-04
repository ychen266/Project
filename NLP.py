import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, ne_chunk
from nltk.corpus import stopwords
import string

# Initialize WordNetLemmatizer and NLTK deactivation words
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

# Enter text
text = "What is the output kinetic energy when Base mass is 5 and other input values are default?"

# Sentence syncopation
sentences = nltk.sent_tokenize(text)

# Word cut (remove punctuation)
tokens = [word for sent in sentences for word in word_tokenize(sent) if word.isalpha()]

# Identifying stopwords
stopwords_removed = [word for word in tokens if word.lower() not in stop_words]

# Lemmatization
lemmatized_words = [lemmatizer.lemmatize(word, wordnet.VERB) for word in stopwords_removed]


# Dependency analysis
pos_tags = pos_tag(lemmatized_words)
dependency_analysis = nltk.ne_chunk(pos_tags)

# Finding noun phrases
noun_phrases = []
for subtree in dependency_analysis.subtrees():
    if subtree.label() == 'NP':
        noun_phrase = ' '.join(word for word, pos in subtree.leaves())
        noun_phrases.append(noun_phrase)

# Named Entity Recognition (NER)
named_entities = []
for chunk in nltk.ne_chunk(pos_tags):
    if hasattr(chunk, 'label') and chunk.label() == 'NE':
        named_entity = ' '.join(c[0] for c in chunk)
        named_entities.append(named_entity)


print("Original Text:", text)
print("Sentence syncopation:", sentences)
print("Text after removal of punctuation:", tokens)
print("Text after removal of deactivated words:", stopwords_removed)
print("Text after Lemmatization:", lemmatized_words)

print("Dependency analysis:", pos_tags)

print("Dependency analysis:", dependency_analysis)
print("Noun phrases:", noun_phrases)
print("Named entities:", named_entities)
