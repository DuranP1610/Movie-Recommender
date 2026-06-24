import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("movies.csv")

df["overview"] = df["overview"].fillna("")

tfidf = TfidfVectorizer(stop_words= "english")
tfidf_matrix = tfidf.fit_transform(df["overview"])

cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

indices = pd.Series(df.index, index=df["title"]).drop_duplicates()

def recommend(title, top_n=10):
    if title not in indices:
        return f"Movie '{title}' not found in dataset."

    idx = indices[title]

    # Get similarity scores for this movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort by similarity score
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Top results
    sim_scores = sim_scores[1:top_n + 1]

    movie_indices = [i[0] for i in sim_scores]

    return df[["title", "rating"]].iloc[movie_indices]

if __name__ == "__main__":
    print(recommend("Supergirl"))