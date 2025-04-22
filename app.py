from flask import Flask
from ProductionCode.filter import Filter
from ProductionCode.data import Data

app = Flask(__name__)

# Create a single Data instance globally
data = Data()

@app.route("/")
def home():
    return (
        "<h1>Welcome to the Streaming Media Filter API</h1>"
        "<p>To filter by actor, go to <code>/actor/&lt;actor_name&gt;</code></p>"
        "<p>Example: <a href='/actor/Brendan Gleeson'>/actor/Brendan Gleeson</a></p>"
    )

@app.route('/actor/<actor_name>')
def filter_by_actor(actor_name):
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
