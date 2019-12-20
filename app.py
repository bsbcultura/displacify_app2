from flask import Flask, render_template, url_for, request

# NLP pakages
import spacy
from spacy import displacy

# Markdown pakages to convert HTML result
from flaskext.markdown import Markdown

# Init NLP object with english model 'en'
#### nlp = spacy.load('en_core_web_sm') ## OK em localhost
import en_core_web_sm # Para heroku
nlp = en_core_web_sm.load()

# Init App
app = Flask(__name__)
Markdown(app)

HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem; margin-bottom: 2.5rem">{}</div>"""

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/extract', methods=["GET","POST"])
def extract():
	if request.method == 'POST':
		rawtext = request.form['rawtext']
		docx = nlp(rawtext)
		html = displacy.render(docx, style='ent')
		html = html.replace("\n\n", "\n")
		result = HTML_WRAPPER.format(html)

	return render_template('results.html', rawtext=rawtext, result=result)



if __name__ == '__main__':
	app.run(debug = True)