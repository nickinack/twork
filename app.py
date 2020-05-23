from flask import Flask , render_template , request

app = Flask(__name__)
app.secret_key = 'test'  # app.secret_key = 'a26d9e7eff0d4dba88d35458034c57b1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, '../dbase.sqlite')


# Import database and models
from models import db, User
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)