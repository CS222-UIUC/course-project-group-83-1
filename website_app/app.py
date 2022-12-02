from flask import Flask, render_template
import scrape

app = Flask(__name__)

@app.route('/')
def index():
    """ alter this code to get the keyword submission
    if request.method == 'POST':
        keyword = request.form['keyword']
        start_date = request.form['start_date']
        
        # (keyword, start_date, end_date, output_file)
        if not title or (len(keyword) < 3):
            flash('valid keyword is required!')
        else:
            # use scrape here
    """
    return render_template('index.html')

if __name__ == "__main__":
    app.run()