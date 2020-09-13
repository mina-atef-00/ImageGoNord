from flask import Flask
from flask import jsonify, abort
from flask import request
from flask_cors import CORS, cross_origin
from flask_restx import Api, Resource
from ImageGoNord import GoNord, NordPaletteFile

API_VERSION = 'v1'
API_VERSION_URL = '/' + API_VERSION

app = Flask(__name__)
cors = CORS(app)
api = Api(app, version=API_VERSION, prefix=API_VERSION_URL)


@api.route('/status')
class StatusEndpoint(Resource):
    def get(self):
        return {'ok': True}


@app.route(API_VERSION_URL + "/convert", methods=["POST"])
def convert():
    go_nord = setup_instance(request)
    output_path = ''
    response = {'success': True}

    if request.files.get('file'):
        image = go_nord.open_image(request.files.get('file').stream)
    elif request.form.get('file_path'):
        image = go_nord.open_image(request.form.get('file_path'))
    elif request.form.get('b64_input'):
        image = go_nord.base64_to_image(request.form.get('b64_input'))
    else:
        abort(400, 'You need to provide at least a valid image or image path')

    if request.form.get('width') and request.form.get('height'):
        image = go_nord.resize_image(image)

    if request.form.get('output_path'):
        output_path = request.form.get('output_path')

    image = go_nord.convert_image(image, save_path=output_path)

    if request.form.get('b64_output'):
        b64_image = go_nord.image_to_base64(image, 'jpeg')
        base64_img_string = b64_image.decode('UTF-8')
        response['b64_img'] = base64_img_string

    return jsonify(response)


@app.route(API_VERSION_URL + "/quantize", methods=["POST"])
def quantize():
    go_nord = setup_instance(request)
    output_path = ''
    response = {'success': True}

    if request.files.get('file') != None:
        image = go_nord.open_image(request.files.get('file').stream)
    elif request.form.get('file_path') != None:
        image = go_nord.open_image(request.form.get('file_path'))
    elif request.form.get('b64_input') != None:
        image = go_nord.base64_to_image(request.form.get('b64_input'))
    else:
        abort(400, 'You need to provide at least a valid image or image path')

    if request.form.get('width') and request.form.get('height'):
        image = go_nord.resize_image(image)

    if request.form.get('output_path') != None:
        output_path = request.form.get('output_path')

    image = go_nord.quantize_image(image, save_path=output_path)

    if request.form.get('b64_output') != None:
        b64_image = go_nord.image_to_base64(image, 'jpeg')
        base64_img_string = b64_image.decode('UTF-8')
        response['b64_img'] = base64_img_string

    return jsonify(response)


def setup_instance(req):
    go_nord = GoNord()

    hex_colors = []
    if req.form.get('colors') != None:
        hex_colors = req.form.get('colors').split(',')

    if len(hex_colors) > 0:
        go_nord.reset_palette()
        for hex_color in hex_colors:
            go_nord.add_color_to_palette(hex_color)

    if req.form.get('is_avg') != None:
        go_nord.enable_avg_algorithm()

    if req.form.get('avg_box_width') != None and req.form.get('avg_box_height') != None:
        go_nord.set_avg_box_data(int(req.form.get('avg_box_width')), int(req.form.get('avg_box_height')))

    if req.form.get('blur') != None:
        go_nord.enable_gaussian_blur()

    return go_nord


if __name__ == '__main__':
    app.run(port=8000, host='0.0.0.0', threaded=True)
