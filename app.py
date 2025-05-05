"""
app.py

This is a Flask app for filtering streaming media entries
based on actor names and movie genres. 
"""
from flask import Flask
from ProductionCode.filter import Filter
from ProductionCode.data import Data

app = Flask(__name__)

data = Data()

@app.route("/")
def home():
    """
    Home route that provides instructions on how to use the website
    """
    return (
        "<h1>Welcome to Streaming Media</h1>"
        "<p>To filter by actor, go to <code>/actor/&lt;actor_name&gt;</code></p>"
        "<p>Example: <a href='/actor/Brendan Gleeson'>/actor/Brendan Gleeson</a></p>"
        "<p>To filter by genre, go to <code>/genre/&lt;genre_name&gt;</code></p>"
        "<p>Example: <a href='/genre/Drama'>/genre/Drama</a></p>"
    )

@app.route('/actor/<actor_name>')
def filter_by_actor(actor_name):
    """
    Filters media entries by actor name and formats the results
    """
    results = get_filtered_by_actor(actor_name)
    return format_media_results(results, f"actor: {actor_name}")

@app.route('/genre/<genre_name>')
def filter_by_genre(genre_name):
    """
    Filters media entries by genre and formats the results
    """
    results = get_filtered_by_genre(genre_name)
    return format_media_results(results, f"genre: {genre_name}")


def get_filtered_by_actor(actor_name):
    """
    Uses the Filter class to filter media entries by actor name
    """
    f = Filter(data)
    f.filter_by_actor(actor_name)
    return f.get_filtered_media_dict()

def get_filtered_by_genre(genre_name):
    """
    Uses the Filter class to filter media entries by genre
    """
    f = Filter(data)
    f.filter_by_category(genre_name)
    return f.get_filtered_media_dict()

def format_media_results(results, label):
    """
    Formats a dictionary of media entries as text string
    """
    if not results:
        return f"No entries found for {label}"

    lines = [f"Results for {label}"]
    for media in results.values():
        lines.append(f"- {media.title} ({media.release_year})")
    return "\n".join(lines)

if __name__ == "__main__":
    app.run(debug=True)
