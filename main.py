from flask import Flask
from flask_cors import CORS
from flask_restful import Api, Resource

import contest_details_soup
import soup

app = Flask(__name__)
CORS(app)
api = Api(app)


class UserInfo(Resource):
    def get(self, platform, username):
        user = soup.Data(username)
        return user.get_details(platform)


class Contest(Resource):
    def get(self):
        contest = contest_details_soup.Data()
        return contest.get_contest()


api.add_resource(UserInfo, "/api/<string:platform>/<string:username>")
api.add_resource(Contest, "/api/all")


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
