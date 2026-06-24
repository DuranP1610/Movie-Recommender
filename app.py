import streamlit as st
import pandas as pd
from recommender import recommend

st.title("🎬 Movie Recommender")

df = pd.read_csv("movies.csv")

movie_list = df["title"].dropna().sort_values().unique()

selected_movie = st.selectbox("Choose a movie:", movie_list)

if st.button("Recommend"):
    results = recommend(selected_movie)

    st.subheader("Top Recommendations")
    st.dataframe(results)