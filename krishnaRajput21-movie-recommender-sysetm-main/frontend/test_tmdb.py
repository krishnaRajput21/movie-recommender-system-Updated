# test_tmdb.py
import requests

TMDB_API_KEY = "4a8a9ef55022158be86fe6ff86e238b3"
r = requests.get(f"https://api.themoviedb.org/3/movie/1726?api_key={TMDB_API_KEY}")
print("STATUS:", r.status_code)
print("BODY:", r.text[:300])