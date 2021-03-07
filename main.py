from flask import Flask, render_template, render_template, request
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy
from os import path

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Habitat(db.Model):
    name = db.Column(db.Text, primary_key=True)
    users = db.Column(db.Integer, nullable=False)
    posts = db.relationship('Post', backref='habitat', lazy=True)
    # def __repr__(self):
    #     return f'"name":{self.name}, "users":{self.users}, "posts":{self.posts}'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    habitat_name = db.Column(db.Text, db.ForeignKey('habitat.name'), nullable=False)

if not path.exists('./database.db'):
    db.create_all()
post_parser = reqparse.RequestParser()
post_parser.add_argument('title', type=str, required=True)
post_parser.add_argument('content', type=str, required=True)

post_fields = {
    'title' : fields.String,
    'content' : fields.String,
    'habitat' : fields.String
}

habitat_fields = {
    'id' : fields.Integer,
    'name': fields.String,
    'users': fields.Integer,
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
        result = Habitat.query.filter_by(name=h).first()
        if result:
            abort(409, message='habitat already exists')
        result = Habitat(name=h, users=0)
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
            args = post_parser.parse_args()   
            post = Post(id=len(Post.query.all()), title=args['title'], content=args['content'], habitat_name=h)
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


api.add_resource(DataBase, '/database/<string:h>')
api.add_resource(HabitatDB, '/database/<string:h>/<string:t>')


@app.route('/<name>')
def habitat(name):
    return render_template('habitat.html', habitat=name)
@app.route('/discussion')
def discussion():
    return render_template('discussion.html', habitat='test')
@app.route('/<name>/posts/<post>')
def post(name, post):
    return render_template('post.html', habitat=name, postID=post)

if __name__ == '__main__':
    app.run(debug=True)