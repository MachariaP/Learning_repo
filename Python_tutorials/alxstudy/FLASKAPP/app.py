from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy

# create an instance of the Flask class
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mysite.db'
db = SQLAlchemy(app)

" flask app "
class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text(500), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/index')
def home(): # view home
    return render_template('index.html')

@app.route('/about')
def about(): # view about
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact(): # view contact
    if request.method == 'POST':
        try:
            name=request.form['name']
            email=request.form['email']
            message=request.form['message']

            new_message = Message(name=name, email=email, message=message)
            db.session.add(new_message)
            db.session.commit()

            return redirect(url_for('home'))
        except Exception as e:
            print(f"An error occurred while trying to add a new message: {e}")
            db.session.rollback()
    else:
        return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
