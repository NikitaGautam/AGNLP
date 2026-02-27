
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

df = pd.read_csv("scopus-abstracts-temp.csv", sep='\t',header=0)
titles = df.iloc[:,1].values.tolist()
model = SentenceTransformer('bert-base-nli-mean-tokens')
title_embeddings = model.encode(titles)
similarity_matrix = cosine_similarity(title_embeddings, title_embeddings)

not_similar_indexes = []
for index, item in enumerate(titles):
    similarity_scores = similarity_matrix[index]
    similarity_scores.sort()
    scores = similarity_scores[-2]  # Exclude the query title itself
    if scores < 0.9:
        not_similar_indexes.append(index)

out_df = df.iloc[not_similar_indexes]
out_df.to_csv("/AG/App/FlaskApp/senegal/scopus-abstracts.csv", sep='\t',index=None)

