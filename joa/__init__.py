from flask import Flask
from flask import render_template, redirect, url_for
import json
import os
from collections import OrderedDict
app = Flask(__name__)

@app.template_filter('dpo_data_links')
def dpo_data_links(data, chapter=None):
    def l_to_ul(l):
        out = u'<ul>'
        for i in l:
            print i
            out += u"<li><span class='fileName'>{}</span></li>".format(
                    i.split(' ', 1)[0].split('/')[-1]
                    )
        out += u'</ul>'
        return out
    def dict_to_ul(d, depth=0):
        out = u'<ul>'
        for k, v in d.iteritems():
            if type(v) is dict:
                out += u"<li>{}  \u2192<ul>".format(k)
                out += dict_to_ul(v, depth+1)
                out += u"</ul></li>"
            if type(v) is list:
                out += u'<li>{} \u2192'.format(k)
                out += l_to_ul(v)
                out += u'</li>'
        out += u'</ul>'
        return out

    if chapter:
        a = u'''<h3 id="data-files-supplied-for-chapter-2-exercises">Data files
        supplied for Chapter {} exercises:</h3>'''.format(chapter)
        d = data[str(chapter)][str(chapter)]
        if type(d) is dict:
            a += dict_to_ul(d)
        if type(d) is list:
            a += l_to_ul(d)
        a += u"""Download: <a
        href='/zipped/dpo/{ch}/DPO_data_chapter_{ch}.zip'>Chapter {ch} Data
        Files</a>""".format(ch=chapter)
        return a
    splits = data.split(' ', 1)
    a = u'<a href="{0}">{1}</a> '.format(splits[0], splits[0].split('/')[-1])
    if len(splits) > 1:
        a +=  splits[1]
    return a

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

@app.route("/joa")
@app.route("/joa/<path:page>")
def joa(page=None):

    # hacking due to rails translation
    subpages = ['index']
    template = 'joa/index.html'
    if page:
        subpages = [page.split('.')[0]]
        template = "joa/" + page

    return render_template(template, page='joa', subpages=subpages)

@app.route("/tour")
@app.route("/tour/<int:page>")
def tour(page=None):
    if page is None:
        return redirect("/tour/1")

    template = 'tour/{}.html'.format(page)

    return render_template(template, page='tour', subpages=['page'], tour=page)

@app.route("/dpo/")
@app.route("/dpo/<path:page>")
def dpo(page=None):
    template = 'dpo/index.html'
    data = None
    do = OrderedDict()
    sort = []
    if page:
        if not page.endswith('.html'):
            page += ".html"
        subpages = [page.split('.')[0]]
        template = "dpo/" + page

    #hacks hacks hacks
    # the DPO examples should just be rewritten in sphinx
    path = os.path.dirname(os.path.abspath(__file__))
    data = os.path.join(path, 'data', 'dpo_data_files.json')
    with open(data, 'r') as f:
        data = json.load(f)
    order = ['2', '3', '4', '6', '7', '9', '10', '11', '12', '13',
            '14', 'S6']
    for o in order:
        do[o] = {o: data[o]}

    return render_template(template, data=do)

@app.route("/dpo_examples/<path:page>")
def dpo_rewrite(page=None):
    #some awesome routing hacks
    return redirect("static/dpo_examples/" + page)

@app.route("/data")
@app.route("/data/<subpage>")
@app.route("/data/<subpage>/<subsubpage>")
def data(subpage=None, subsubpage=None):
    template = 'data/index.html'
    if subpage.startswith('best'):
        template = 'data/best.html'
    if subpage.startswith('other'):
        template = 'data/other/index.html'
        if subsubpage:
            template = 'data/other/' + subsubpage
    data=None
    return render_template(template, page='data', data=data)

if __name__ == "__main__":
    app.run(debug=True)
