import streamlit as st 
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=338ca044a93564180e73a75dc91751cd&language=en-US'
    try:
        response = requests.get(url, timeout=5)  # Add timeout to prevent hanging
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        return "https://image.tmdb.org/t/p/w500" + data.get('poster_path', ''), data.get('runtime', 'N/A')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/500", "N/A"  # Fallback image and runtime

def fetch_cast(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=338ca044a93564180e73a75dc91751cd&language=en-US'
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        cast = [member['name'] for member in data.get('cast', [])[:5]]  # Fetch top 5 cast members
        return ', '.join(cast)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching cast: {e}")
        return "Cast information not available"

def format_runtime(minutes):
    if minutes == "N/A" or minutes is None:
        return "Runtime not available"
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}h {mins}m"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    runtimes = []
    casts = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id 
        
        recommended_movies.append(movies.iloc[i[0]].title) 
        # Fetch movie details
        poster, runtime = fetch_poster(movie_id)
        runtime_formatted = format_runtime(runtime)
        cast = fetch_cast(movie_id)
        recommended_movies_posters.append(poster)
        runtimes.append(runtime_formatted)
        casts.append(cast)
    
    return recommended_movies, recommended_movies_posters, runtimes, casts

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a Movie Option',
    movies['title'].values
)

if st.button('Recommend'):
    show_recommendations = st.checkbox("Show/Hide Recommendations", value=True)
    
    if show_recommendations:
        names, posters, runtimes, casts = recommend(selected_movie_name)
        col1, col2, col3, col4, col5 = st.columns(5)
        
        for i, col in enumerate([col1, col2, col3, col4, col5]):
            with col:
                # Movie name in yellow
                st.markdown(f"<span style='color:green; font-weight:bold;'>{names[i]}</span>", unsafe_allow_html=True)
                st.image(posters[i])
                
                # Runtime in yellow
                st.markdown(f"<span style='color:grey;'>Runtime: {runtimes[i]}</span>", unsafe_allow_html=True)
                
                # Cast information
                st.caption(f"Cast: {casts[i]}")
                
                # Add download option
                st.markdown(
                    f"<a href='https://moviesmod.red/page/9/' target='_blank' style='text-decoration:none;'><b>⬇️ Download</b></a>",
                    unsafe_allow_html=True
                )
        
        # Add thank you message at the bottom
        st.markdown("<br><hr><center><b>Thank you for visiting my site! 😊</b></center>", unsafe_allow_html=True)
        
        # Add call option with phone emoji
        st.markdown(
            "<center><b>📞 Call at: <a href='tel:+9337758716'>9337758716</a></b></center>",
            unsafe_allow_html=True
        )
