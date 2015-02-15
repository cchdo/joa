from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route("/")
@app.route("/home")
@app.route("/home/<path:page>")
def index(page=None):

    # hacking due to rails translation
    subpages = ['index']
    template = 'home/index.html'
    if page:
        subpages = [page.split('.')[0]]
        template = "home/" + page

    return render_template(template, page='home', subpages=subpages)

if __name__ == "__main__":
    app.run(debug=True)
