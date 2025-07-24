from flask import Flask, render_template, request, redirect, url_for
import redis

app = Flask(__name__)

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

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
    return render_template('index.html')

@app.route('/results')
def results():
    cats = int(r.get("votes:cats") or 0)
    dogs = int(r.get("votes:dogs") or 0)
    return render_template('results.html', votes={'cats': cats, 'dogs': dogs})

if __name__ == '__main__':
    app.run(debug=True)

