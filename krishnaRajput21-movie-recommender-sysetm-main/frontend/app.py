import streamlit as st
import requests
import time

# Hugging Face par backend aur frontend ek hi jagah chalenge, isliye localhost (127.0.0.1) use kar rahe hain
BACKEND_BASE_URL = "http://127.0.0.1:8000"   
API_URL = f"{BACKEND_BASE_URL}/recommend"

st.set_page_config(
    page_title="Enterprise AI Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 AI-Powered Movie Recommender")
st.markdown("Powered by **FastAPI**, **SentenceTransformers**, and **Chroma Vector DB**")

TMDB_API_KEY = "4a8a9ef55022158be86fe6ff86e238b3"

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except Exception as e:
        print(f"Error fetching poster: {e}")
    return None

def call_backend(params, retries=6, delay=8):
    """Backend connection retry logic."""
    last_error = None
    for attempt in range(retries):
        try:
            return requests.get(API_URL, params=params, timeout=15)
        except requests.exceptions.ConnectionError as e:
            last_error = e
            time.sleep(delay)
    raise last_error

st.sidebar.header("Search Settings")
top_k = st.sidebar.slider("Number of Recommendations", min_value=1, max_value=10, value=5)

with st.form(key="search_form"):
    query = st.text_input(
        "Enter a Movie Name or Semantic Plot Description:",
        placeholder="e.g., Avatar, or 'space travel and futuristic galaxy wars'"
    )
    submitted = st.form_submit_button("Get Recommendations", type="primary")

if submitted:
    if not query.strip():
        st.warning("Please enter a movie title or plot description!")
    else:
        with st.spinner("Finding best recommendations for you..."):
            try:
                response = call_backend({"query": query, "top_k": top_k})

                if response.status_code == 200:
                    data = response.json()
                    recommendations = data.get('recommendations', [])

                    st.success(f"Top {len(recommendations)} Recommendations for '{query}':")

                    if recommendations:
                        cols = st.columns(len(recommendations))
                        for idx, item in enumerate(recommendations):
                            movie_id = item['movie_id']
                            title = item['title']
                            poster_url = fetch_poster(movie_id)
                            with cols[idx]:
                                if poster_url:
                                    st.image(poster_url, use_container_width=True)
                                else:
                                    st.warning("Poster not found")
                                st.subheader(title)
                    else:
                        st.info("No recommendations found.")
                else:
                    st.error(f"Backend Error: {response.json().get('detail', 'Unknown error')}")

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend. Make sure the server is running.")