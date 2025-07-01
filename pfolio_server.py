# Portfolio Website Python Server

from flask import Flask, request, redirect, render_template, url_for
from datetime import datetime
import csv

app = Flask(__name__)

@app.route('/')
def my_home():
    return render_template('index.html')

@app.route('/<string:page_name>')
def html_pager(page_name):
    return render_template(page_name)

def write_to_file(data):
    with open('./database.txt', mode = 'a') as database:
        email = data['email']
        name = data['name']
        message =  data['message']
        file = database.write(f'\n {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, {email}, {name}, {message}')

def write_to_csv(data):
    with open('./database.csv', mode = 'a', newline='') as database2:
        email = data['email']
        name = data['name']
        message =  data['message']
        csv_writer = csv.writer(database2, delimiter = ',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), email, name, message])

# this bit of code allows us to grab data from our webpage
# form for potential employers to contact us for work:
@app.route('/submit_form', methods=['POST'])
def submit_form():
    print(request.method)
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_file(data)
            write_to_csv(data)
            return redirect('/thankyou.html')
        except:
            return 'Did not save to database.'
    else:
        return 'Something went wrong. Try again.'

# The try/except structure allows us to catch an error
# for the purpose of writing to a database and
# troubleshooting errors.