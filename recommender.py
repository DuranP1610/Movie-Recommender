import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = None
cosine_sim = None
indices = None


def build_model():
    global df, cosine_sim, indices

    df = pd.read_csv("movies.csv")

    df["title"] = df["title"].str.strip().str.lower()
    df["overview"] = df["overview"].fillna("")

    # IMPORTANT: reset FIRST and clean data BEFORE anything else
    df = df.drop_duplicates(subset="title").reset_index(drop=True)

    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(df["overview"])

    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    indices = pd.Series(df.index, index=df["title"])

def recommend(title, top_n=10):
    if df is None:
        build_model()

    title = title.strip().lower()

    if title not in indices:
        return df.head(0)

    idx = int(indices[title])

    sim_scores = list(enumerate(cosine_sim[idx].ravel()))
    sim_scores = sorted(sim_scores, key=lambda x: float(x[1]), reverse=True)
    sim_scores = sim_scores[1:top_n+1]

    movie_indices = [i[0] for i in sim_scores]

    # 🔥 SAFETY GUARD (important)
    movie_indices = [i for i in movie_indices if i < len(df)]

    return df.iloc[movie_indices][["title", "rating"]]