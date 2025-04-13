# import streamlit as st
# import pickle
# import pandas as pd
# import requests
# from fuzzywuzzy import process
# from dotenv import load_dotenv
# import os
# from download import download_file

# load_dotenv()

# st.set_page_config(
#     page_title="🎬 Movie Recommender",
#     page_icon="🎥",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# download_file()  # Ensure the similarity.pkl file is downloaded
# # Load data
# movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
# movies = pd.DataFrame(movies_dict)
# similarity = pickle.load(open('similarity.pkl', 'rb'))

# # Extract all unique genres (assuming 'genres' column exists as list)
# all_genres = sorted({genre for sublist in movies['genres'] for genre in sublist}) if 'genres' in movies else []
# all_genres.insert(0, "All")
# # Function to fetch movie details from TMDB API
# def fetch_movie_details(movie_id):
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={os.getenv('API_KEY')}&language=en-US"
#     response = requests.get(url)
#     if response.status_code != 200:
#         return None, None, None, None, None
#     data = response.json()
#     poster = "https://image.tmdb.org/t/p/w500/" + data.get('poster_path', "")
#     official_link = f"https://www.themoviedb.org/movie/{movie_id}"
#     return poster, data.get('overview', "No overview available."), data.get('release_date', "N/A"), data.get('vote_average', "N/A"), official_link
# # Recommend logic
# def recommend(movie, selected_genre="All"):
#     try:
#         movie_index = movies[movies['title'] == movie].index[0]
#     except IndexError:
#         return [], [], [], [], [], [], []

#     distances = similarity[movie_index]
#     scores = list(enumerate(distances))
#     sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

#     recommended_movies = []
#     posters = []
#     overviews = []
#     release_dates = []
#     ratings = []
#     sim_scores = []
#     official_links = []

#     for idx, score in sorted_scores[1:]:
#         row = movies.iloc[idx]

#         # Genre filtering (if applicable)
#         if selected_genre != "All" and selected_genre not in row['genres']:
#             continue

#         poster, overview, release, rating, official_link = fetch_movie_details(row.movie_id)
#         recommended_movies.append(row.title)
#         posters.append(poster)
#         overviews.append(overview)
#         release_dates.append(release)
#         ratings.append(rating)
#         sim_scores.append(round(score * 100, 2))
#         official_links.append(official_link)

#         if len(recommended_movies) == 5:
#             break

#     return recommended_movies, posters, overviews, release_dates, ratings, sim_scores, official_links

# # App UI
# st.title("🎬 Movie Recommendation System")

# # Add the CSS for the "Watch Here" button
# st.markdown("""
#     <style>
#         .watch-button {
#             background-color: #ffcc00;/*yellow*/
#             color: white;
#             padding: 10px 20px;
#             border: none;
#             border-radius: 5px;
#             text-align: center;
#             display: inline-block;
#             font-size: 16px;
#             cursor: pointer;
#             transition: background-color 0.3s ease;
#         }
        
#         .watch-button:hover {
#             background-color: #000000;
#         }

#         .watch-button:active {
#             background-color: #3e8e41;
#         }
#     </style>
# """, unsafe_allow_html=True)

# # Genre filter dropdown
# selected_genre = st.selectbox("🎞️ Filter by Genre", all_genres)

# selected_movie_name = st.selectbox(
#     "🎥 Search or select a movie you like:", 
#     movies['title'].values, 
#     index=0,
#     label_visibility="visible"
# )

# # User input (with fuzzy matching)
# user_input = st.text_input("🔍 Type a movie name:", "")
# if user_input:
#     selected_movie_name = process.extractOne(user_input, movies['title'].values)[0]
#     st.success(f"🔎 Interpreted as: **{selected_movie_name}**")

# # Recommend button
# if st.button("🎯 Recommend") and selected_movie_name:
#     names, posters, overviews, release_dates, ratings, scores, links = recommend(selected_movie_name, selected_genre)

#     if not names:
#         st.warning("No matching recommendations found. Try a different genre.")
#     else:
#         cols = st.columns(5)
#         for i in range(5):
#             with cols[i]:
#                 st.image(posters[i], use_column_width=True)
#                 st.markdown(f"<div><b>{names[i]}</b></div>", unsafe_allow_html=True)
#                 st.markdown(f"📅 {release_dates[i]} | ⭐ {ratings[i]}", unsafe_allow_html=True)
#                 st.markdown(f"Match: {scores[i]}%", unsafe_allow_html=True)
#                 st.markdown(f'<a href="{links[i]}" class="watch-button" target="_blank">Watch Here</a>', unsafe_allow_html=True)
#                 with st.expander("📝 Overview"):
#                     st.write(overviews[i])
# else:
#     st.info("Type a movie name and click Recommend to see suggestions.")



import streamlit as st
import pickle
import pandas as pd
import requests
from fuzzywuzzy import process
from dotenv import load_dotenv
import os
from download import download_file

load_dotenv()

st.set_page_config(
    page_title="🎬 Movie Recommender",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

download_file()  # Ensure the similarity.pkl file is downloaded

# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Extract all unique genres
all_genres = sorted({genre for sublist in movies['genres'] for genre in sublist}) if 'genres' in movies else []
all_genres.insert(0, "All")

# Fetch movie details and official link
def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={os.getenv('API_KEY')}&language=en-US"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch details for {movie_id}. Status code: {response.status_code}")
        return None, "No overview available.", "N/A", "N/A", "#"
    data = response.json()
    poster_path = data.get('poster_path')
    print("Poster path:", poster_path)
    poster = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else None
    print("Poster URL:", poster)
    print("https://image.tmdb.org/t/p/w500/"+poster_path)
    official_link = f"https://www.themoviedb.org/movie/{movie_id}"
    return poster, data.get('overview', "No overview available."), data.get('release_date', "N/A"), data.get('vote_average', "N/A"), official_link

# Recommend logic
def recommend(movie, selected_genre="All"):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
    except IndexError:
        return [], [], [], [], [], [], []

    distances = similarity[movie_index]
    scores = list(enumerate(distances))
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

    recommended_movies = []
    posters = []
    overviews = []
    release_dates = []
    ratings = []
    sim_scores = []
    official_links = []

    for idx, score in sorted_scores[1:]:
        row = movies.iloc[idx]

        # Genre filtering
        if selected_genre != "All" and selected_genre not in row['genres']:
            continue

        poster, overview, release, rating, official_link = fetch_movie_details(row.movie_id)
        recommended_movies.append(row.title)
        posters.append(poster)
        overviews.append(overview)
        release_dates.append(release)
        ratings.append(rating)
        sim_scores.append(round(score * 100, 2))
        official_links.append(official_link)

        if len(recommended_movies) == 5:
            break

    return recommended_movies, posters, overviews, release_dates, ratings, sim_scores, official_links

# App UI
st.title("🎬 Movie Recommendation System")

# Custom CSS for buttons
st.markdown("""
    <style>
        .watch-button {
            background-color: #ffcc00;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            text-align: center;
            display: inline-block;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        
        .watch-button:hover {
            background-color: #000000;
        }

        .watch-button:active {
            background-color: #3e8e41;
        }
    </style>
""", unsafe_allow_html=True)

# Genre filter
selected_genre = st.selectbox("🎞️ Filter by Genre", all_genres)

# Movie selection
selected_movie_name = st.selectbox(
    "🎥 Search or select a movie you like:", 
    movies['title'].values, 
    index=0,
    label_visibility="visible"
)

# Fuzzy matching for manual text input
user_input = st.text_input("🔍 Type a movie name:", "")
if user_input:
    selected_movie_name = process.extractOne(user_input, movies['title'].values)[0]
    st.success(f"🔎 Interpreted as: **{selected_movie_name}**")

# Recommendation button
if st.button("🎯 Recommend") and selected_movie_name:
    names, posters, overviews, release_dates, ratings, scores, links = recommend(selected_movie_name, selected_genre)

    if not names:
        st.warning("No matching recommendations found. Try a different genre.")
    else:
        cols = st.columns(5)
        for i in range(len(names)):
            with cols[i]:
                if posters[i]:
                    st.image(posters[i], use_container_width=True)
                else:
                    st.warning("🎞️ No poster available.")
                st.markdown(f"<div><b>{names[i]}</b></div>", unsafe_allow_html=True)
                st.markdown(f"📅 {release_dates[i]} | ⭐ {ratings[i]}", unsafe_allow_html=True)
                st.markdown(f"Match: {scores[i]}%", unsafe_allow_html=True)
                st.markdown(f'<a href="{links[i]}" class="watch-button" target="_blank">Watch Here</a>', unsafe_allow_html=True)
                with st.expander("📝 Overview"):
                    st.write(overviews[i])
else:
    st.info("Type a movie name and click Recommend to see suggestions.")
