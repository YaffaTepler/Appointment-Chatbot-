from flask import Flask, request, render_template, jsonify

from modules.google_api import get_available_days, get_available_slots_for_day
from modules.calendar import add_appointment


app = Flask(__name__)

@app.route('/')
def index():
    available_days = get_available_days()
    return render_template('index.html', available_days=available_days)

@app.route('/slots')
def slots():
    day = request.args.get('day')
    if not day:
        return jsonify({"error": "No day provided"}), 400
    slots = get_available_slots_for_day(day)
    return jsonify(slots)

@app.route('/book', methods=['POST'])
def book():
    name = request.form['name']
    mail = request.form['mail']
    date = request.form['date']
    time = request.form['time']
    datetime_str = f"{date}T{time}"
    success, message = add_appointment(datetime_str, name, mail)
    return render_template('confirmation.html', message=message)


if __name__ == '__main__':
    app.run(debug=True)
