from flask import Flask, request, render_template, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'plantguard-secret-key-2024'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    return redirect(url_for('success'))

@app.route('/success')
def success():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
