from flask import Blueprint, jsonify, render_template
from .openai_utils import get_image_description, chat_with_openai
import os

bp = Blueprint('routes', __name__, template_folder='templates')


@bp.route('/')
def index():
    return "Welcome to ScreenshotSorter!"


@bp.route('/test-vision')
def test_vision():
    # Hardcoded path for testing
    directory = r"C:\Users\Shubham Tyagi\Pictures\Screenshots"
    file_name = "Screenshot (12).png"
    image_path = os.path.join(directory, file_name)
    openapi_key = "------ADD KEY-------"
    description = get_image_description(openapi_key, image_path)

    # Render the response in a simple HTML template
    return render_template('response.html', title='Vision API Response', response=description)


@bp.route('/test-chat')
def test_chat():
    # Hardcoded message for testing
    message = "Translate 'Hello, world!' to Hindi"
    openapi_key = "--------ADD KEY-------"
    instructions = "Please translate the following text to Hindi accurately."

    response = chat_with_openai(openapi_key, message, instructions)

    # Render the response in a simple HTML template
    return render_template('response.html', title='Chat API Response', response=response)
