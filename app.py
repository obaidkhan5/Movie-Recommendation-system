import streamlit as st
import pickle
import pandas as pd
import requests
from sklearn.metrics.pairwise import linear_kernel

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="AI Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

# ======================================================
# CUSTOM CSS
# ======================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(to right, #141E30, #243B55);
    color: white;
}

.main-title {
    text-align: center;
    font-size: 60px;
    font-weight: bold;
    color: white;
    margin-top: -30px;
}

.sub-title {
    text-align: center;
    color: #d3d3d3;
    font-size: 20px;
    margin-bottom: 40px;
}

.movie-card {
    background-color: rgba(255,255,255,0.08);
    border-radius: 15px;
    padding: 10px;
    text-align: center;
    transition: 0.3s;
    height: 100%;
}

.movie-card:hover {
    transform: scale(1.03);
    background-color: rgba(255,255,255,0.15);
}

.movie-title {
    font-size: 16px;
    font-weight: bold;
    color: white;
    margin-top: 10px;
}

.stButton>button {
    width: 100%;
    background-color: #E50914;
    color: white;
    border: none;
    border-radius: 10px;
    height: 50px;
    font-size: 18px;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #ff1f1f;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# LOAD PKL FILES
# ======================================================

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# ======================================================
# FIX INDEXING
# ======================================================

movies.reset_index(drop=True, inplace=True)

# ======================================================
# TMDB API KEY
# ======================================================

API_KEY = "YOUR_TMDB_API_KEY"

# ======================================================
# FETCH MOVIE POSTER
# ======================================================

def fetch_poster(movie_title):

    try:

        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"

        response = requests.get(url)

        data = response.json()

        if len(data['results']) == 0:
            return "https://via.placeholder.com/500x750?text=No+Image"

        poster_path = data['results'][0].get('poster_path')

        if poster_path is None:
            return "https://via.placeholder.com/500x750?text=No+Image"

        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path

        return full_path

    except:

        return "https://via.placeholder.com/500x750?text=No+Image"

# ======================================================
# RECOMMENDATION FUNCTION
# ======================================================

def recommend(movie):

    try:

        movie_index = movies[
            movies['title'] == movie
        ].index[0]

    except:

        return [], []

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:11]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:

        movie_title = movies.iloc[i[0]].title

        recommended_movies.append(movie_title)

        poster = fetch_poster(movie_title)

        recommended_posters.append(poster)

    return recommended_movies, recommended_posters

# ======================================================
# HEADER
# ======================================================

st.markdown(
    '<p class="main-title">🎬 AI Movie Recommendation System</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub-title">Content-Based Filtering using Machine Learning</p>',
    unsafe_allow_html=True
)

# ======================================================
# SEARCH BOX
# ======================================================

movie_list = sorted(movies['title'].values)

selected_movie = st.selectbox(
    "🔍 Search Movie",
    movie_list,
    index=0
)

# ======================================================
# BUTTON
# ======================================================

if st.button("🎥 Recommend Movies"):

    names, posters = recommend(selected_movie)

    if len(names) == 0:

        st.error("Movie not found.")

    else:

        st.subheader(f"Top Recommendations for: {selected_movie}")

        # FIRST ROW

        cols = st.columns(5)

        for idx in range(5):

            with cols[idx]:

                st.image(
                    posters[idx],
                    use_container_width=True
                )

                st.markdown(
                    f"""
                    <div class="movie-card">
                        <div class="movie-title">
                            {names[idx]}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.write("")

        # SECOND ROW

        cols2 = st.columns(5)

        for idx in range(5, 10):

            with cols2[idx - 5]:

                st.image(
                    posters[idx],
                    use_container_width=True
                )

                st.markdown(
                    f"""
                    <div class="movie-card">
                        <div class="movie-title">
                            {names[idx]}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# ======================================================
# FOOTER
# ======================================================

st.write("")
st.write("")

st.markdown("""
<hr>
""", unsafe_allow_html=True)