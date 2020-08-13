from flask import Flask
from flask import jsonify, abort
from flask import request
from flask_cors import CORS, cross_origin

from ImageGoNord import GoNord, NordPaletteFile

API_VERSION = '/v1'

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route(API_VERSION + "/status", methods=["GET"])
@cross_origin()
def get_api_status():
  return jsonify({'ok': True})

@app.route(API_VERSION + "/quantize", methods=["POST"])
@cross_origin()
def quantize():
  return jsonify({'ok': True})

@app.route(API_VERSION + "/convert", methods=["POST"])
@cross_origin()
def convert():
  return jsonify({'ok': True})  

if __name__ == '__main__':
	app.run(port=8000, threaded=True)