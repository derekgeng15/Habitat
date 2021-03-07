from flask import Flask, render_template, render_template, request, session, redirect, url_for
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
from os import path

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = 'secret lol'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class Habitat(db.Model):
    name = db.Column(db.Text, primary_key=True)
    users = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Integer, nullable=False)
    posts = db.relationship('Post', backref='habitat', lazy=True)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    posts = db.relationship('Post', backref='user', lazy=True)
    def check_password(self, password):
        return self.password == password

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    habitat_name = db.Column(db.Text, db.ForeignKey('habitat.name'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)



if not path.exists('./database.db'):
    db.create_all()

post_parser = reqparse.RequestParser()
post_parser.add_argument('title', type=str, required=True)
post_parser.add_argument('content', type=str, required=True)

habitat_parser = reqparse.RequestParser()
habitat_parser.add_argument('description', type=str, required=True)
habitat_parser.add_argument('users', type=str, required=True)

newpost_parser = reqparse.RequestParser()
newpost_parser.add_argument('title', type=str, required=True)
newpost_parser.add_argument('content', type=str, required=True)
newpost_parser.add_argument('userID', type=int, required=True)

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', type=str)
login_parser.add_argument('email', type=str)
login_parser.add_argument('password', type=str)

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str)
user_parser.add_argument('id', type=int)

post_fields = {
    'title' : fields.String,
    'content' : fields.String,
    'habitat' : fields.String,
    'user' : fields.String
}

habitat_fields = {
    'id' : fields.Integer,
    'name': fields.String,
    'users': fields.Integer,
    'posts' : fields.Nested(post_fields),
    'description' : fields.String
}

user_fields = {
    'id' : fields.Integer,
    'username' : fields.String,
    'email' : fields.String,
    'password' : fields.String,
    'posts' : fields.Nested(post_fields)
}


class DataBase(Resource):
    @marshal_with(habitat_fields)
    def get(self, h):
        result = Habitat.query.filter_by(name=h).first()
        if not result:
            abort(404, message='habitat does not exist')
        return result

    @marshal_with(habitat_fields)
    def post(self, h):
        args = habitat_parser.parse_args()
        result = Habitat.query.filter_by(name=h).first()
        if result:
            abort(409, message='habitat already exists')
        result = Habitat(name=h,  description=args['description'], users=args['users'].count(',') + 1)
        db.session.add(result)
        db.session.commit()
        return result

class HabitatDB(Resource):
    
    @marshal_with(habitat_fields)
    def get(self, h, t):
        result = Habitat.query.filter_by(name=h).first()
        if not result:
            abort(404, message='habitat does not exist')
        return result

    @marshal_with(habitat_fields)
    def put(self, h, t):
        result = Habitat.query.filter_by(name=h).first()
        if not result:
            abort(404, message='habitat does not exist')
        if t == 'users':
            result.users += 1
        if t == 'posts':
            args = newpost_parser.parse_args()  
            post = Post(id=len(Post.query.all()), title=args['title'], content=args['content'], habitat_name=h, user_id=args['userID'])
            db.session.add(post)
        db.session.commit()
        return result
    @marshal_with(habitat_fields)
    def delete(self, h, t):
        result = Habitat.query.filter_by(name=h).first()
        if not result:
            abort(404, message='habitat does not exist')
        if t == 'users' and result.users > 0:
            result.users -= 1
        db.session.commit()
        return result

class UserDB(Resource):

    @marshal_with(user_fields)
    def get(self, u):
        args = user_parser.parse_args()
        result = User.query.filter_by(username=u)
        if not result:
            abort(404, message='user does not exists')
        return result
    @marshal_with(user_fields)
    def post(self, u):
        args = login_parser.parse_args()
        result = User.query.filter_by(username=u).first()
        if result:
            abort(409, message='user already exists')
        user = User(id=len(User.query.all()), username=u, email=args['email'], password=args['password'])
        db.session.add(user)
        login_user(user, remember=True)
        db.session.commit()
        return user
    @marshal_with(user_fields)
    def put(self, u):
        args = login_parser.parse_args()
        result = User.query.filter_by(username=u).first()
        if not result:
            abort(404, message='user does not exists')
        if not result.check_password(args['password']):
            abort(4625, message='incorrect password')
        login_user(result, remember=True)
        db.session.commit()
        return result

api.add_resource(DataBase, '/database/<string:h>')
api.add_resource(HabitatDB, '/database/<string:h>/<string:t>')
api.add_resource(UserDB, '/database/users/<string:u>')

@login_manager.user_loader
def load_user(user):
    return User.query.get(user)

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('login'))
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        return {'message' : 'post lol'}
    elif request.method == 'GET':
        return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/users/<user>')
def user(user):
    if User.query.filter_by(username=user).first():
        return render_template('index.html', user=user)
    else:
        return 'no'
@app.route('/<name>')
def habitat(name):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('habitat.html', habitat=name, user=current_user)

@app.route('/<name>/discussion')
def discussion(name):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('discussion.html', habitat=name, user=current_user)

@app.route('/<name>/posts/<post>')
def post(name, post):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('post.html', habitat=name, postID=post, user=current_user)

@app.route('/<name>/newpost')
def newpost(name):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('newpost.html', habitat=name, user=current_user)

if __name__ == '__main__':
    app.run(debug=True)