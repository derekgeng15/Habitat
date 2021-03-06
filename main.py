from flask import Flask, render_template, render_template
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# db.SQLAlchemy(app)

@app.route('/')
def home():
    return render_template('habitat.html')

if __name__ == '__main__':
    app.run(debug=True)