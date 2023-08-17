from flask import Flask, jsonify, request
from flask_restful import Api,Resource, reqparse

app = Flask(__name__);

api = Api(app);

names = {
    "vince":{"age":23,"gender":"male"},
    "carol":{"age":24, "gender":"female"}
};

#There will be details in the Request that need to be properly parsed if I need to use
#any details 
putargs = reqparse.RequestParser()

#I need to parse the filed like "Likes", "Name of the video" and "How many views the video has"
putargs.add_argument("name",type=str, help="Name of the video")
putargs.add_argument("views",type=int,help="No. of views the video has garnered")
putargs.add_argument("likes",type=int,help="No. of likes the video has")

videos={};
class Names(Resource):
    def get(self,name):
        return names[name]

class ytvideos(Resource):
    def get(self, videoid):
        return videos[videoid]
    
    def put(self, videoid):
        args = putargs.parse_args()
        videos[videoid] = args;
        return {videoid:args} 

api.add_resource(Names,'/homepage/<string:name>')
api.add_resource(ytvideos,'/ytvideo/<int:videoid>')
# api.add_resource(ytvideos,'/ytvideo/<int:video_id>')
if __name__ == "__main__":
    app.run(debug=True)