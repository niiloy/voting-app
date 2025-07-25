from flask import Flask, render_template, request, redirect, url_for
import redis
import time
import os

app = Flask(__name__)

# Connect to Redis
while True:
    try:
        r = redis.Redis(host="redis", port=6379, db=0)
        if r.ping():
            print("Connected to Redis!")
            break
    except redis.exceptions.ConnectionError:
        print("Waiting for Redis...")
        time.sleep(1)
#r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

# Initialize vote keys if not present
if not r.exists("votes:cats"):
    r.set("votes:cats", 0)
if not r.exists("votes:dogs"):
    r.set("votes:dogs", 0)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        vote = request.form['vote']
        if vote in ['cats', 'dogs']:
            r.incr(f'votes:{vote}')
        return redirect(url_for('results'))
    container_id = os.uname()[1]
    return render_template('index.html', container_id=container_id)

@app.route('/results')
def results():
    cats = int(r.get("votes:cats") or 0)
    dogs = int(r.get("votes:dogs") or 0)
    container_id = os.uname()[1]
    return render_template('results.html', votes={'cats': cats, 'dogs': dogs}, container_id=container_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

