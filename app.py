from flask import Flask, render_template, request, redirect
from events import formatted_data, event_interested_in

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/events', methods=['POST'])
def events():
    city = request.form['city']
    date = request.form['date']
    print(f"Received data: City - {city}, Date - {date}")

    events_data = formatted_data(city, date)
    print(events_data)
    if not city or not date: #exceptions
        return redirect('/error_page')

    return render_template('events.html', city=city, events_data=events_data)

@app.route('/error_page')
def error_page():
    return render_template('error_page.html')


if __name__ == '__main__':
    app.run(debug=True)
