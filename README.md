# Image Augmentation API Service With CLI  API-Testing Tool

<br>

## About The Project

Project presents an implementation of REST service letting augment basic image features, accompanied with CLI tool to consume it.

### Features

#### Augmentation API Service

* Image Operations
    * Resizing
    * Cropping
    * Rotation
    * Lossy (Re)compression
    * Negative (Color Inversion)

* API Endpoints

```sh
/resize?width=<int>&height=<int>
/crop?left=<int>&upper=<int>&right=<int>&lower=<int>
/rotate?angle=<0-360>
/compress?level=<1-100>
/invert
```

* Service processes data in below formats
    * jpg
    * png
    * bmp

#### CLI API-Testing Tool

* Commands letting consume the API service
* Options to point input and output file paths
* Included CLI help easing understanding CLI elements and command construction
* Handling input data
    1. Image read from a file in one of below formats
        * jpg
        * png
        * bmp
    2. POST request containing JSON with encoded base64 image

* Handling output data
    1. Receiving response containing augmented image
    2. Saving the image to a file in original format unless JPEG compression
       applied

### Stack

* Interpreter
    * Python 3.10
* Containerization
    * Docker
* Web Framework
    * Flask
* Imaging Library
    * Pillow
* CLI Toolkit
    * click

## Getting Started

### Prerequisites

* Docker
* Python 3.10 with pip
* virtualenv tool

### Setting Up The Project

#### Setting Up The Service

##### Build docker image and run the container, e.g.:

```sh
docker build --tag img-augment-app .
```

#### Setting Up The CLI API-Testing Tool

```sh
cd augmentation_tool
virtualenv venv; source venv/bin/activate
pip install --no-cache-dir -r requirements.txt
```

## Usage

### API Service Start Example

```sh
docker run --name img-augment-app -p 5000:5000 img-augment-app
```

### CLI Tool Usage

```sh
python augment.py <operation_name> <arguments> <options>
```

<details>
	<summary>Possible Operation Names</summary>
	<ul>
		<li>resize</li>
		<li>crop</li>
		<li>rotate</li>
		<li>compress</li>
		<li>invert</li>
	</ul>
</details>

<details>
	<summary>Possible Arguments</summary>
	<var>
		<ul>
			<li>width:int</li>
			<li>height:int</li>
			<li>left:int</li>
			<li>upper:int</li>
			<li>right:int</li>
			<li>lower:int</li>
			<li>angle:int (0-360)</li>
			<li>level:int (1-100)</li>
		</ul>
	</var>
</details>

<details>
	<summary>Possible Options</summary>
	<ul>
		<li>
			<code>--input=&ltstr&gt</code> (required input file path)
		</li>
		<li>
			<code>--output=&ltstr&gt</code> (required output file path)
		</li>
		<li>
			<code>--uri=&ltstr&gt</code>
			(address:port; default:
			<code>--uri http://0.0.0.0:5000</code>)
		</li>
	</ul>
</details>

#### Usage Examples

```sh
python augment.py resize 200 100 --input test_images/img.jpg --output out.jpg
```

```sh
python augment.py crop 100 200 300 400 --input test_images/img.jpg --output out.jpg
```

```sh
python augment.py rotate 90 --input test_images/img.jpg --output out.jpg
```

```sh
python augment.py compress 10 --input test_images/img.jpg --output out.jpg
```

```sh
python augment.py invert --input test_images/img.jpg --output out.jpg  --uri http://0.0.0.0:8000
```

##### Help Access Example

```sh
$ python augment.py crop --help

Usage: augment.py crop [OPTIONS] LEFT UPPER RIGHT LOWER

  Crop image using coordinates represented by arguments: left, upper, right,
  lower. Points (x1,y1)=(left,upper) and (x2,y2)=(right,lower) correspond to
  box corners. The inside of the box is the crop operation output.

Options:
  --uri TEXT     API service <address:port>  [default: http://0.0.0.0:5000]
  --output TEXT  output filepath  [required]
  --input TEXT   input filepath  [required]
  --help         Show this message and exit.
```
