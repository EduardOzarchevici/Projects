from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    views = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name)= {self.name}, views= {self.views} , likes= {self.likes} )"

#db.create_all()

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is requried", required=True)
video_put_args.add_argument("views", type=int, help="Views of video are required", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video required", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is requried")
video_update_args.add_argument("views", type=int, help="Views of video are required")
video_update_args.add_argument("likes", type=int, help="Likes on the video required")


def abort_if_video_id_doesnt_exist(video_id):
    video = VideoModel.query.filter_by(id=video_id).first()
    if not video:
        abort(404, message="Could not find video id...")

def abort_if_video_exists(video_id):
    video = VideoModel.query.filter_by(id=video_id).first()
    if video:
        abort(409, message="Video already exists")



class Video(Resource):
    def get(self, video_id):
        abort_if_video_id_doesnt_exist(video_id)
        video = VideoModel.query.filter_by(id=video_id).first()
        return {"id": video.id, "name": video.name, "views": video.views, "likes": video.likes}

    def put(self, video_id):
        abort_if_video_exists(video_id)
        args = video_put_args.parse_args()
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return {"id": video.id, "name": video.name, "views": video.views, "likes": video.likes}, 201

    def delete(self, video_id):
        abort_if_video_id_doesnt_exist(video_id)
        video = VideoModel.query.filter_by(id=video_id).first()
        db.session.delete(video)
        db.session.commit()
        return '', 204

    def patch(self, video_id):
        abort_if_video_id_doesnt_exist(video_id)
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        print("Args: ", args)
        print(result)

        if args.get("name") is not None:
            result.name = args["name"]
        if args.get("likes") is not None:
            result.likes = args["likes"]
        if args.get("views") is not None:
            result.views = args["views"]

        db.session.commit()
        print(result)
        return {'message':'Video modified succefuly!'}

api.add_resource(Video, "/video/<int:video_id>")
if __name__ == "__main__":
    app.run(debug=True)


