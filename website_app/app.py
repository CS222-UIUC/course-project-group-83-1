from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import scrape

app = Flask(__name__)

@app.route('/', methods=('GET', 'POST'))
def index():
    # alter this code to get the keyword submission
    # include a way to access previous keyword searches
    print("hi")
    if request.method == 'POST':
        
        keyword = request.form['keyword']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        output_tag = "dummy_name.json" # try to make this have a unique id fo every process
        # scrape_twitter(keyword, start_date, end_date, output_file)
        if not keyword or (len(keyword) < 3):
            flash('valid keyword is required!')
        else:
            # 
            # ----- check if this keyword has been used before
                # ask whether the person would like to just load the results
                # from the previous search
            
            #------ other wise conduct an entirely new scrape of twitter
            
            pass
            #scrape_twitter(keyword, start_date, end_date, output_file)
    
    return render_template('index.html')

if __name__ == "__main__":
    app.run()