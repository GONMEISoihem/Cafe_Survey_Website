from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from flask_bootstrap import Bootstrap5
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired('Please enter cafe name')])
    location = StringField('Location', validators=[DataRequired(),
                                                   URL(require_tld=True, message='Please enter a valid location')])
    open = StringField('Open', validators=[DataRequired()])
    close = StringField('Close', validators=[DataRequired()])
    # Dropdown fields for ratings with emojis
    coffee_rating_choices = [
        '☕',
        '☕☕',
        '☕☕☕',
        '☕☕☕☕',
        '☕☕☕☕☕'
    ]

    wifi_rating_choices = [
        '💪',
        '💪💪',
        '💪💪💪',
        '💪💪💪💪',
        '💪💪💪💪💪'
    ]

    power_rating_choices = [
        '🔌',
        '🔌🔌',
        '🔌🔌🔌',
        '🔌🔌🔌🔌',
        '🔌🔌🔌🔌🔌'
    ]

    Coffee_Rating = SelectField('Coffee Rating', choices=coffee_rating_choices, validators=[DataRequired()])
    WiFi_strength = SelectField('Wi-Fi Rating', choices=wifi_rating_choices, validators=[DataRequired()])
    Power = SelectField('Power Availability', choices=power_rating_choices, validators=[DataRequired()])

    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        cafe = request.form['cafe']
        location = request.form['location']
        open_time = request.form['open']
        close = request.form['close']
        coffee_rating = request.form['Coffee_Rating']
        wifi_rating = request.form['WiFi_strength']
        power_rating = request.form['Power']

        with open('cafe-data.csv', mode='a', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([cafe, location, open_time, close, coffee_rating, wifi_rating, power_rating])

            return redirect('/cafes')

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
