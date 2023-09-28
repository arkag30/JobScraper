from flask import Flask, render_template, request
import pandas as pd  # Import Pandas
from jobspy import scrape_jobs
# ...

app = Flask(__name__)

def find_jobs(term,type,loc='India',links=True,results=5,easy=True):
    try:
        jobs = scrape_jobs(site_name=['linkedin'],location=loc,search_term=term,hyperlinks=links,results_wanted=results,easy_apply=easy,job_type=type)
        return jobs
    except Exception as e:
        jobs = {'Jobs': ['No Jobs Found']}
        return pd.DataFrame(jobs)


@app.route('/', methods=['GET', 'POST'])
def index():
    job_listings = pd.DataFrame()  # Initialize an empty DataFrame
    
    if request.method == 'POST':
        location = request.form['location']
        search_term = request.form['search_term']
        hyperlinks = 'hyperlinks' in request.form
        results_wanted = int(request.form['results_wanted'])
        easy_apply = 'easy_apply' in request.form
        job_type = request.form['job_type']
        if job_type == 'Internship':
            easy_apply = False
        job_listings = find_jobs(search_term,job_type,location,hyperlinks,results_wanted,easy_apply)
    return render_template('index.html', job_listings=job_listings.to_html(classes='table table-striped'))

if __name__ == '__main__':
    app.run(debug=True)
