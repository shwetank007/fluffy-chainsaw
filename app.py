import os
import requests
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from rq import Queue
from rq.job import Job
from worker import conn

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

q = Queue(connection=conn)

from models import Result

def count_words_at_url(url):
    resp = requests.get(url)
    return len(resp.text.split())

@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = {}
    print('Hi')
    if request.method == "POST":
        from app import count_words_at_url

        url = request.form['url']
        job = q.enqueue_call(
            func=count_words_at_url, args=(url,), result_ttl=5000
        )
        print(job.get_id())
    return render_template('index.html', errors=errors, results=results)

if __name__ == '__main__':
    app.run()
