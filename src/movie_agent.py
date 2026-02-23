import json
from pathlib import Path
import requests


class MovieAgent:
    def __init__(self, data_path):
        self.data_path = Path(data_path)
        self.movies = self.load_movies()

    def load_movies(self):
        if not self.data_path.exists():
            return []
        with open(self.data_path, "r") as file:
            return json.load(file)

    def save_movies(self):
        with open(self.data_path, "w") as file:
            json.dump(self.movies, file, indent=2)

    def add_movie(self, title, genre, rating, year, watched=False):
        movie = {
            "title": title,
            "genre": genre,
            "rating": rating,
            "year": year,
            "watched": watched
        }
        self.movies.append(movie)
        self.save_movies()

    def list_movies(self):
        return self.movies

    def search_by_genre(self, genre):
        return [
            movie for movie in self.movies
            if movie["genre"].lower() == genre.lower()
        ]

    def recommend(self, min_rating=8):
        return [
            movie for movie in self.movies
            if movie["rating"] >= min_rating
        ]

    def fetch_movie_details(self, title):
        url = "https://ghibliapi.vercel.app/films"
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return None

        movies = response.json()

        for movie in movies:
            if movie["title"].lower() == title.lower():
                return {
                    "title": movie["title"],
                    "genre": "Animation",
                    "rating": float(movie["rt_score"]) / 10,
                    "year": int(movie["release_date"]),
                    "watched": False
                }
        return None


# ---------------- MAIN PROGRAM ---------------- #

if __name__ == "__main__":
    agent = MovieAgent("data/movies.json")

    movie_name = input("\nEnter a movie name to fetch details: ")

    movie = agent.fetch_movie_details(movie_name)

    if movie:
        print("\nMovie found from API:")
        print(movie)

        save = input("Do you want to save this movie? (y/n): ")

        if save.lower() == "y":
            agent.add_movie(**movie)
            print("✔ Movie saved successfully!")
    else:
        print("\nMovie not found in external source")
