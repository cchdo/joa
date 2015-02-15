from flask import Flask
from flask import render_template, redirect, url_for
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

@app.route("/tour")
@app.route("/tour/<int:page>")
def tour(page=None):
    if page is None:
        return redirect("/tour/1")

    template = 'tour/{}.html'.format(page)

    return render_template(template, page='tour', subpages=['page'], tour=page)

if __name__ == "__main__":
    app.run(debug=True)
