from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import scrape, graph
import sentiment_analysis as sen

app = Flask(__name__)
app.config['SECRET_KEY'] = 'admin123_foobar'

def main_process(submit_data):
    keyword, start_date, end_date, output_tag = submit_data
    polarity_tags = ["Tweet", "Polarity", "Subjectivity"]
    
    scraped_data_folder = "scraped_data/"
    full_polarity_folder = "processed_data/"
    average_folder = "averaged_data/"
    images_folder = "data_images/"

    # change this part, put the "scraped" etc, tags at the beginning
    scraped_output_file = scraped_data_folder + "scraped_" + output_tag + ".json"
    full_polarity_file = full_polarity_folder + "processed_" + output_tag + ".json"
    avg_polarity_file = average_folder + "averaged_" + output_tag + ".json"

    scrape.scrape_twitter(keyword, start_date, end_date, scraped_output_file)
    
    sen.main_process_polarity(scraped_output_file, 
                        polarity_tags, full_polarity_file, avg_polarity_file)
    
    # currently using the full_polarity file
    graph.visualize_data(full_polarity_file, images_folder + output_tag)
    




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
            # deal with the invalid keyword here
            # probably should deal with invalid dates too...?
            pass
        elif not start_date or not end_date:

            pass
        else:
            # 
            # ----- check if this keyword has been used before
                # ask whether the person would like to just load the results
                # from the previous search
            
            #------ other wise conduct an entirely new scrape of twitter
            submit_data = keyword, start_date, end_date, output_tag
            #main_process(submit_data)
            
    
    return render_template('index.html')

if __name__ == "__main__":
    app.run()