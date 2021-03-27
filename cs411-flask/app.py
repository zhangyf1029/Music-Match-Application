from flask import Flask
from flask import render_template, request
from forms import EventForm
import requests



import os

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/event_call', methods=['GET', 'POST'])
def event_call():
	form = EventForm()
	if request.method == 'POST':

		classificationName = form.classificationName.data
		postalCode = form.postalCode.data

		# params = {
		# 	'api_key': '{PBSmqVGp0ZUUCVC3VKJ3oTH3SWnidD7S}',
		# 	'classificationName': '{music}',
		# 	'countryCode':'{US}',
		# 	'postalCode':'{02215}'
		# }
		
		#url = "https://app.ticketmaster.com/discovery/v2/events.json?apikey=PBSmqVGp0ZUUCVC3VKJ3oTH3SWnidD7S&classificationName=music&countryCode=US&postalCode=02215"

		response = requests.get(f"https://app.ticketmaster.com/discovery/v2/events.json?apikey=PBSmqVGp0ZUUCVC3VKJ3oTH3SWnidD7S&classificationName=music&countryCode=US&postalCode={postalCode}&classificationName={classificationName}")
	
		json_res = response.json()

		return render_template('search_results.html', events = list(json_res["_embedded"]["events"]))
	else:
		return render_template('event_call.html', title='Find events', form=form)

@app.route('/search_results', methods=['POST'])
def search_results():
    return render_template('search_results.html', title='Display events')


@app.route("/register", methods=['POST'])
def register_user():
	try:
		first_name=request.form.get('first_name')
		last_name=request.form.get('last_name')
		email=request.form.get('email')
		password=request.form.get('password')
		birth_date=request.form.get('birth_date')
		hometown=request.form.get('hometown')
		gender=request.form.get('gender')
	except:
		print("couldn't find all tokens") #this prints to shell, end users will not see this (all print statements go to shell)
		return flask.redirect(flask.url_for('register'))
	cursor = conn.cursor()
	test =  isEmailUnique(email)
	if test:
		print(cursor.execute("INSERT INTO Users (first_name, last_name, email, birth_date, hometown, gender,password) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')"
		.format(first_name, last_name, email, birth_date, hometown, gender,password)))
		conn.commit()
		#log user in
		user = User()
		user.id = email
		flask_login.login_user(user)
		return render_template('profile.html', name=email, message='Account Created!')


if __name__ == '__main__':
    app.run()