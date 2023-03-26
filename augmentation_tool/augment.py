from PIL import Image
from io import BytesIO
import requests as req
import click
import base64


def group_options(func):
    options = [click.option('--input', required=True, help='input filepath'),
               click.option('--output', required=True, help='output filepath'),
               click.option('--uri',
                            default='http://0.0.0.0:5000',
                            show_default=True,
                            help='API service <address:port>')]
    for dec in options:
        func = dec(func)
    return func


def read_image(input):
    with open(input, 'rb') as f:
        im = f.read()
    im_b64 = base64.b64encode(im).decode()

    return {'img': im_b64}


def save_img(res, output):
    im_binary = base64.b64decode(res.json()['img'])
    buf = BytesIO(im_binary)
    img = Image.open(buf)
    img.save(output, format=img.format, quality=100)


@click.group()
def cli():
    pass


@cli.command()
@click.argument('width')
@click.argument('height')
@group_options
def resize(width, height, input, output, uri):
    """
    Change image size according to WIDTH and HEIGHT arguments
    """
    res = req.post(f'{uri}/resize?width={width}&height={height}',
                   json=read_image(input))
    save_img(res, output)


@cli.command()
@click.argument('left')
@click.argument('upper')
@click.argument('right')
@click.argument('lower')
@group_options
def crop(left, upper, right, lower, input, output, uri):
    """
    Crop image using coordinates represented by arguments: left, upper, right,
    lower. Points (x1,y1)=(left,upper) and (x2,y2)=(right,lower) correspond
    to box corners. The inside of the box is the crop operation output.
    """
    res = req.post(
        f'{uri}/crop?left={left}&upper={upper}&right={right}&lower={lower}',
        json=read_image(input))
    save_img(res, output)


@cli.command()
@click.argument('angle')
@group_options
def rotate(angle, input, output, uri):
    """
    Rotate image counterclockwise a given angle(argument) in degrees
    """
    res = req.post(f'{uri}/rotate?angle={angle}', json=read_image(input))
    save_img(res, output)


@cli.command()
@click.argument('level')
@group_options
def compress(level, input, output, uri):
    """
    Compress image to JPG format with given level(argument) of sustained
    quality percentage
    """
    res = req.post(f'{uri}/compress?level={level}', json=read_image(input))
    save_img(res, output)


@cli.command()
@group_options
def invert(input, output, uri):
    """
    Invert/Negate image (colors)
    """
    res = req.post(f'{uri}/invert', json=read_image(input))
    save_img(res, output)


if __name__ == '__main__':
    cli()
