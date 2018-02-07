from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
# 
from flask_heroku import Heroku

app = Flask(__name__)
#heroku = Heroku(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/database.db'

db = SQLAlchemy(app)

class Review(db.Model):
	__tablename__ = "review"
	id = db.Column(db.Integer, primary_key=True)
	book_title = db.Column(db.Unicode)
	content = db.Column(db.Unicode)

class Contact(db.Model):
	__tablename__ = "contact"
	id = db.Column(db.Integer, primary_key = True)
	first_name = db.Column(db.Unicode)
	last_name = db.Column(db.Unicode)
	country = db.Column(db.Unicode)
	subject = db.Column(db.Unicode)


db.create_all()

# print(db.session.query(Book).all())

@app.route("/")
def index():
	return render_template("home.html")

@app.route("/books", methods = ['POST', 'GET'])
def books():
	if(request.method=='GET'):
		reviews = db.session.query(Review).limit(5).all()
		return render_template("Books.html", reviews = reviews)
	else:
		book_title = request.form['title']
		content = request.form['review']
		review = Review(book_title = book_title, content = content)
		db.session.add(review)
		db.session.commit()
		return redirect(url_for('books'))

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/contact', methods=['POST', 'GET'])
def contact():
	if(request.method=='GET'):
		return render_template('contactus.html')
	else:
		fname = request.form['firstname']
		lname = request.form['lastname']
		country = request.form['country']
		subject = request.form['subject']
		contact = Contact(first_name = fname, last_name=lname, country=country, subject=subject)
		db.session.add(contact)
		db.session.commit()
		return redirect(url_for('contact'))


if __name__=='__main__':
	app.run(debug=True)
