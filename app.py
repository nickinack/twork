from flask import Flask , render_template , request, redirect,url_for,session
from flask import flash
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.security import generate_password_hash , check_password_hash
from flask_login import LoginManager , UserMixin , login_user , login_required , logout_user , current_user 


app = Flask(__name__)
app.secret_key = 'test'
project_dir = os.path.dirname(os.path.abspath(__file__))
# database_file = "sqlite:///{}".format(os.path.join(project_dir, "todo.db"))

database_file = "sqlite:///{}".format(os.path.join(project_dir, "db.sqlite"))
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
# app.config['SQLALCHEMY_BINDS'] = {'user' : user_database_file}


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from models import db, User
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def root():
    return redirect(url_for('index'))


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/add' , methods = ['GET','POST'])
def add():
    if request.form:
        user_input = Todo(text=request.form['text'] , desc=request.form['description'] , deadline = request.form['deadline'] , complete = False)
        db.session.add(user_input)
        if db.session.commit():
            flash("Successful")
        return redirect(url_for('add'))

    return render_template('add_todo.html')


@app.route('/register' , methods = ['GET' , 'POST'])
def register():
    flag = None
    if request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if username is None:
            flag = 'Username is required.'
        elif password is None:
            flag = 'Password is required.'
        elif User.query.filter_by(username=username).first():
            flag = 'Username must be unique'
        elif User.query.filter_by(email=email).first():
            flag = 'Email is already registered'
        else:
            user = User(
                firstname=request.form['firstname'],
                lastname=request.form['lastname'],
                email=request.form['email'],
                username=request.form['username'],
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            print('committed')
            return redirect(url_for('login'))
    
    if flag:
        flash(f'{flag}')
        print(flag)

    return render_template('register.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    flag = None
    if current_user.is_authenticated:
        return render_template('dashboard.html' , username = current_user.firstname)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user is None:
            flag = 'No such user'
        elif not check_password_hash(user.password , password):
            flag = 'Incorrect password'
        
        
        if flag:
            flash(flag)
            print(flag)
        else:
            login_user(user)
            return redirect(url_for('dashboard'))
    
    return render_template('login.html')


@app.route('/dashboard' , methods=('GET', 'POST'))
@login_required
def dashboard():   
    return render_template('dashboard.html' , username=current_user.firstname)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


'''
    ------------- HELPER FUNCTIONS FOR LOGIN MANAGER -------------
'''
@login_manager.user_loader
def user_loader(id):
    if id is not None:
        return User.query.get(id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    flash('You are not authorized to perform that action.')
    return redirect(url_for('login'))

'''
    ------------ END HELPERS -------------------
'''




if __name__ == '__main__':
    app.run(debug=True) 
