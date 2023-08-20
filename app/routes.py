from flask import Flask, render_template, request, redirect, url_for, session

import os
from dotenv import load_dotenv, find_dotenv

from app import app
from app.services.report import astr_report

load_dotenv(find_dotenv())
app.secret_key = os.getenv('SECRET_KEY')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        year = int(request.form['year'])
        month = int(request.form['month'])
        day = int(request.form['day'])
        hour = int(request.form['hour'])
        minute = int(request.form['minute'])
        city = request.form['city']
        
        result_text = astr_report(name, year, month, day, hour, minute, city) 
        session['result_text'] = result_text 
        print("Result text stored in session")
        return redirect(url_for('result'))
    
    return render_template('index.html')

@app.route('/result')
def result():
    result_text = session.get('result_text')
    print("Result text retrieved from session:", result_text)
    return render_template('result.html', result_text=result_text)