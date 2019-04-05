from flask import Flask, url_for, request, render_template, abort, redirect, jsonify
from user import User
from base import Session
import json
import re

application = Flask(__name__)
application.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# This just allows us to do a sanity check to verify that the Flask app is up.
@application.route("/")
def index():
    return "This service is working."

# This URL will return all users.
@application.route("/users")
def users():
	session = Session()
	users = session.query(User).all()
	return jsonify([user.as_dict() for user in users])

# This URL will return details on a specific user.
@application.route("/users/<int:id>")
def user(id):
	session = Session()
	user = session.query(User).get(id)
	if (user is not None):
		return jsonify(user.as_dict())
	else:
		response = {"error": "User not found"}
		return jsonify(response), 500

# GET gives you an HTML form to create a new user (useful for demonstration purposes,
# although a production API might not have this).
# POST saves the user after checking for duplicates.
@application.route("/users/create", methods=['GET', 'POST'])
def create_user():
	if (request.method == 'GET'):
		return render_template('create_user.html')
	elif (request.method == 'POST'):
		
		name = request.form['name']
		phone = request.form['phone']
		
		# Remove everything except for digits
		p = re.compile(r"[^0-9]")
		phone = re.sub(p, '', phone)
		
		if (len(phone) != 10):
			response = {"error": "Phone number is wrong length"}
			return jsonify(response), 500

		# Check for a duplicate phone number
		session = Session()
		duplicate = session.query(User).filter(User.phone == phone).all()
		if (len(duplicate) > 0):
			response = {"error": "This phone number is already in the system"}
			return jsonify(response), 500

		# All tests have passed, so create and insert the user.
		new_user = User(name, phone)
		
		session.add(new_user)
		session.commit()
		session.close()

		# After we have finished inserting the new user,
		# redirect to show all users including the one we just inserted.
		return redirect(url_for('users'))

@application.route("/users/delete/<int:id>")
def delete(id):
	session = Session()
	session.query(User).filter(User.id == id).delete()
	session.commit()
	session.close()

	# Show the list, now without the user we just deleted
	return redirect(url_for('users'))

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()


