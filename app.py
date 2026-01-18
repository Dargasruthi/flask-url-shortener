from flask import Flask, render_template, request
from models import db, URL
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
db.init_app(app)

# Create database
with app.app_context():
    db.create_all()

# Generate short code
def generate_short_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=5))

@app.route('/', methods=['GET', 'POST'])
def home():
    short_url = None
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_code = generate_short_url()

        new_url = URL(original_url=long_url, short_url=short_code)
        db.session.add(new_url)
        db.session.commit()

        short_url = "http://127.0.0.1:5000/" + short_code

    return render_template('home.html', short_url=short_url)

@app.route('/history')
def history():
    urls = URL.query.all()
    return render_template('history.html', urls=urls)

if __name__ == '__main__':
    app.run(debug=True)
