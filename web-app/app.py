import streamlit as st
import json
from data import KNearestNeighbours
from operator import itemgetter
from PIL import Image


# Load data and movies list from corresponding JSON files
with open(r'data.json', 'r+', encoding='utf-8') as f:
    data = json.load(f)
with open(r'titles.json', 'r+', encoding='utf-8') as f:
    movie_titles = json.load(f)


def knn(test_point, k):
    # Create dummy target variable for the KNN Classifier
    target = [0 for item in movie_titles]
    # Instantiate object for the Classifier
    model = KNearestNeighbours(data, target, test_point, k=k)
    # Run the algorithm
    model.fit()
    # Distances to most distant movie
    max_dist = sorted(model.distances, key=itemgetter(0))[-1]
    # Print list of 10 recommendations < Change value of k for a different number >
    table = list()
    for i in model.indices:
        # Returns back movie title and imdb link
        table.append([movie_titles[i][0], movie_titles[i][2]])
    return table


if __name__ == '__main__':
    genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
              'Fantasy', 'Film-Noir', 'Game-Show', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News',
              'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Thriller', 'War', 'Western']

    movies = [title[0] for title in movie_titles]
    st.markdown("<h1 style='text-align: center;'>Movie-Shala</h1>", unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center;'>Grab your popcorns, as we recommend the best</h2>",
                unsafe_allow_html=True)
    # st.header('Which Movie To Watch Today?'
    # loading image from system
    img = Image.open('pic1.png')
    st.image(img, use_column_width=True)

    st.markdown(
        "<h5 style='text-align: center;'>Want to watch top rated movies and be the shinning one among your peers. Yes "
        "you have landed on the right place. It consists of redirecting IMDB links to particular movies in order to "
        "give you a review of selected movies." "\nYou can even sort movies based on genres and IMDb score.</h5>",
        unsafe_allow_html=True)

    st.markdown("<h6>Select on which basis you'd like movie recommendations.</h6>", unsafe_allow_html=True)
    apps = ['--Select--', 'Movie based', 'Genre based']
    app_options = st.selectbox('Select recommendation mode:', apps)

    if app_options == 'Movie based':
        movie_select = st.selectbox('Select movie:', ['--Select--'] + movies)
        if movie_select == '--Select--':
            pass
        else:
            n = st.number_input('Number of movie recommendations:', min_value=5, max_value=20, step=1)
            genres = data[movies.index(movie_select)]
            test_point = genres
            table = knn(test_point, n)
            for movie, link in table:
                # Displays movie title with link to imdb
                st.markdown(f"[{movie}]({link})")
    elif app_options == apps[2]:

        options = st.multiselect('Select genres:', genres)
        if options:
            imdb_score = st.slider('IMDb score:', 1, 10, 8)
            st.write("You can customize IMDB score")
            n = st.number_input('Number of movie recommendations:', min_value=5, max_value=20, step=1)
            test_point = [1 if genre in options else 0 for genre in genres]
            test_point.append(imdb_score)
            table = knn(test_point, n)
            for movie, link in table:
                # Displays movie title with link to imdb
                st.markdown(f"[{movie}]({link})")

        else:
            st.write(
                "Welcome To Genre based portal. Scan movies through your favourite genre")
