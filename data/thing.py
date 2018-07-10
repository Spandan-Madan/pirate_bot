import numpy as np
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer

x = TfidfVectorizer()
x.fit_transform(['The car is driven on the road.', 'The truck is driven on the highway.'])

tfidf = x
str = 'The car is driven on the road. The truck is driven on the highway.'
response = tfidf.transform([str])
feature_names = tfidf.get_feature_names()
feature_array = np.array(tfidf.get_feature_names())
tfidf_sorting = np.argsort(response.toarray()).flatten()[::-1]

for col in response.nonzero()[1]:
    print feature_names[col], ' - ', response[0, col]