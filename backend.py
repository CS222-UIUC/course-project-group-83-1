from flask import Flask, request, render_template
import scrape
app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('website.html')

@app.route('/', methods=['POST'])
def my_form_post():
    keyword = request.form['keyword']
    start_date = request.form['start_date']
    end_date = request.form['start_date']
    scrape.scrape_test(keyword, start_date, end_date, "blah.json")