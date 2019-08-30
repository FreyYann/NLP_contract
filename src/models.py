from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from nltk.stem.snowball import SnowballStemmer
from nltk import WordNetLemmatizer, pos_tag, word_tokenize
from nltk.corpus import wordnet
from nltk.stem.porter import *
from nltk.stem import *
import pickle
from gensim import corpora,similarities,models
from sklearn.metrics import classification_report

def compare_similarity(text,stemmer,label_dict,dictionary):
    test_data_1 = text
    test_data_1=re.sub("[0-9]+|[,\.\-%#\\“\”'\/\$]|\)|\(|\t|$",' ',\
                       test_data_1.lower()).split()
    test_data_1=[stemmer.stem(x.lower()) for x in test_data_1]
    test_corpus_1 = dictionary.doc2bow(test_data_1)

    test_corpus_tfidf_1=tfidf_model[test_corpus_1]
    # return similarity[test_corpus_tfidf_1]
    return [(label_dict[t[0]],t[1]) for t in similarity[test_corpus_tfidf_1]]

if __name__=='__main__':

    label_dict = {0: 'insurance',
                  1: 'payment|pay|bill|billing',
                  2: 'remedy',
                  3: 'solicitation|solicit',
                  4: 'termination|terminate'}

    with open('../data/contract/docs/df.pkl', 'rb') as f:
        df = pickle.load(f)

    stemmer = PorterStemmer()
    corpora_documents = []
    # plain_text_list = [re.sub("[0-9]+|[,\.\-%#\\“\”'\/\$]|\)|\(|\t|$",' ',x.lower()).split() \
    #                    for x in df.content]
    plain_text_insurance = ' '.join(df[df.label == 'insurance'].content)
    plain_text_pay = ' '.join(df[df.label == 'payment|pay|bill|billing'].content)
    plain_text_remedy = ' '.join(df[df.label == 'remedy'].content)
    plain_text_solicitation = ' '.join(df[df.label == 'solicitation|solicit'].content)
    plain_text_termination = ' '.join(df[df.label == 'termination|terminate'].content)

    plain_text = [plain_text_insurance, plain_text_pay, \
                  plain_text_remedy, plain_text_solicitation, plain_text_termination]

    plain_text = [re.sub("[0-9]+|[,\.\-%#\\“\”'\/\$\)\(]|\t", '', x.lower()) \
                                  for x in plain_text]

    plain_text=[x.split() for x in plain_text]

    for p in plain_text:
        corpora_documents.append([stemmer.stem(w) for w in p])

    dictionary = corpora.Dictionary(corpora_documents)
    corpus = [dictionary.doc2bow(text) for text in corpora_documents]
    tfidf_model = models.TfidfModel(corpus)
    corpus_tfidf = tfidf_model[corpus]

    similarity = similarities.Similarity('Similarity-tfidf-index',
                                         corpus_tfidf, num_features=2500)

    similarity.num_best = 5

    # for it, row in df.iterrows():
    #     if it<50:
    #         print(compare_similarity(row.content,stemmer,label_dict,dictionary)[0],row.label)
    preds=[compare_similarity(x,stemmer,label_dict,dictionary)[0][0] for x in df.content ]
    print(classification_report(df.label, preds))
        # break\