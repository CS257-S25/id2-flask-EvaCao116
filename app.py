"""
This is a Flask app for filtering streaming media entries
based on actor names. The app provides routes to filter media by actor and 
return the filtered results in HTML format.
"""
from flask import Flask
from ProductionCode.filter import Filter
from ProductionCode.data import Data

app = Flask(__name__)

# Create a single Data instance globally
data = Data()

@app.route("/")
def home():
    """
    Home route that provides instructions on how to use the API.
    """
    return (
        "<h1>Welcome to Streaming Media</h1>"
        "<p>To filter by actor, go to <code>/actor/&lt;actor_name&gt;</code></p>"
        "<p>Example: <a href='/actor/Brendan Gleeson'>/actor/Brendan Gleeson</a></p>"
    )

@app.route('/actor/<actor_name>')
def filter_by_actor(actor_name):
    """
    Filters media entries by actor name and formats the results as an HTML list.
    """
    results = get_filtered_by_actor(actor_name)
    return format_media_results_as_html(results, actor_name)


def get_filtered_by_actor(actor_name):
    """
    Uses the Filter class to filter media entries by actor name.
    Returns the filtered dictionary of media objects.
    """
    f = Filter(data)
    f.filter_by_actor(actor_name)
    return f.get_filtered_media_dict()


def format_media_results_as_html(results, actor_name):
    """
    Formats a dictionary of media entries as an HTML string.
    """
    if not results:
        return f"<h2>No entries found for actor: {actor_name}</h2>", 404

    html = f"<h2>Results for actor: {actor_name}</h2><ul>"
    for media in results.values():
        html += f"<li><strong>{media.title}</strong> ({media.release_year})</li>"
    html += "</ul>"
    return html


if __name__ == "__main__":
    app.run(debug=True)
