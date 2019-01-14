import os
import json

from flask import Flask, Response
from flask_restful import Resource, Api
from flask_cors import CORS
from rocketleaguereplayanalysis.data.data_loader import parse_data
from rocketleaguereplayanalysis.util.export import get_all_data


app = Flask(__name__)
CORS(app, origins='http://localhost:3000')
api = Api(app)

@api.resource('/')
class Root(Resource):
    def get(self):
        replays_folder_path = os.path.join(os.path.dirname(__file__), '../test_files')
        replays_paths = []
        for file in os.listdir(replays_folder_path):
            if file.endswith('.json'): # TODO use RocketLeagueReplayParser
                replays_paths.append(os.path.join(replays_folder_path, file))

        # TODO for now just return the first replay
        with open(replays_paths[0]) as data_file:
            data = json.load(data_file)
        frames, actor_data, player_info, team_info, game_event_num = parse_data(data)

        return Response(json.dumps(get_all_data(frames, player_info, team_info)), mimetype='application/json')

if __name__ == "__main__":
    app.run()
