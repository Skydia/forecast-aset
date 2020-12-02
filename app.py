from bokeh.client import pull_session
from bokeh.embed import server_session
from flask import Flask, render_template, url_for
from flask import send_from_directory

app = Flask(__name__)


#BOKEH_URL = "http://127.0.0.1:5006/holoviews_app"
BOKEH_URL = "https://forecast-aset.herokuapp.com/holoviews_app"

# locally creates a page
@app.route('/')
def index():
    index = "home"
    with pull_session(url=BOKEH_URL) as session:
            # generate a script to load the customized session
            script = server_session(session_id=session.id, url=BOKEH_URL)

    return render_template("index.html", script=script, template="Flask", index=index)


if __name__ == '__main__':
    # runs app in debug mode
    app.run(port=5000, debug=True)