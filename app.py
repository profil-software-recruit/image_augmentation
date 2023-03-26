from flask import Flask, request, jsonify
from PIL import Image, ImageOps
from io import BytesIO
import base64

app = Flask(__name__)


def get_request_image(req):
    im_binary = base64.b64decode(req.json['img'])
    buf = BytesIO(im_binary)

    return Image.open(buf)


def get_return_image(img, **kwargs):
    buf = BytesIO()
    img.save(buf, **kwargs)
    img = buf.getvalue()
    img = base64.b64encode(img).decode()

    return jsonify(img=img)


@app.route('/resize', methods=['POST'])
def resize():
    img = get_request_image(request)

    width = request.args.get('width', type=int)
    height = request.args.get('height', type=int)

    return get_return_image(img=img.resize((width, height)),
                            format=img.format)


@app.route('/crop', methods=['POST'])
def crop():
    img = get_request_image(request)

    left = request.args.get('left', type=int)
    upper = request.args.get('upper', type=int)
    right = request.args.get('right', type=int)
    lower = request.args.get('lower', type=int)

    return get_return_image(img=img.crop((left, upper, right, lower)),
                            format=img.format)


@app.route('/rotate', methods=['POST'])
def rotate():
    img = get_request_image(request)

    return get_return_image(
        img=img.rotate(request.args.get('angle', type=int)),
        format=img.format)


@app.route('/compress', methods=['POST'])
def compress():
    return get_return_image(img=get_request_image(request),
                            format='JPEG',
                            quality=request.args.get('level', type=int))


@app.route('/invert', methods=['POST'])
def invert():
    img = get_request_image(request)

    return get_return_image(img=ImageOps.invert(img),
                            format=img.format)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
