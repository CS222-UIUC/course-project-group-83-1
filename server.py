from flask import Flask, render_template
import scrape
import graph3D
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('template.html')

@app.route('/my-link/')
def my_link():
    # scrape.scrape_test("abortion", "2022-04-25", "2022-05-09", "abortion.json")
    graph3D.animate_3D('output=.json', 'abortion')
    return 'here'

if __name__ == '__main__':
  app.run(debug=True)