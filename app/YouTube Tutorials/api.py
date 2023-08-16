from flask import Flask, jsonify, request
from flask_restful import Api,Resource

app = Flask(__name__);

api = Api(app);

names = {
    "vince":{"age":23,"gender":"male"},
    "carol":{"age":24, "gender":"female"}
};

videos={};
class Names(Resource):
    def get(self,name):
        return names[name]

class ytvideos(Resource):
    def get(self, videoid):
        return videos[videoid]
    
    def put(self, video_id):
        return 

api.add_resource(Names,'/homepage/<string:name>')
api.add_resource(ytvideos,'/ytvideo/<int:videoid>')
if __name__ == "__main__":
    app.run(debug=True)