from flask import Blueprint, jsonify, render_template, request
from .openai_utils import get_image_description, chat_with_openai
from .utils import scan_directory_for_images, save_descriptions_map, load_descriptions_map, delete_descriptions_map
import os

bp = Blueprint('routes', __name__, template_folder='templates')
IMAGE_LIMIT = 5
OPEN_AI_KEY = "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"
DIRECTORY_PATH = r"C:\Users\Shubham Tyagi\Pictures\Screenshots"
PROCESSED_IMAGES = set()


@bp.route('/')
def index():
    return "Welcome to ScreenshotSorter!"


@bp.route('/test-vision')
def test_vision():
    # Hardcoded path for testing
    file_name = "Screenshot (12).png"
    image_path = os.path.join(DIRECTORY_PATH, file_name)
    description = get_image_description(OPEN_AI_KEY, image_path)

    # Render the response in a simple HTML template
    return render_template('response.html', title='Vision API Response', response=description)


@bp.route('/test-chat')
def test_chat():
    # Hardcoded message for testing
    instructions = "From the user message, list in csv(no periods at end) important unique keyword labels that will categorize this image description"
    message = r"You've shared a screenshot of a web application interface, likely a section of an investment platform or financial dashboard. The webpage is displaying information about ongoing IPOs (Initial Public Offerings), which is when a company first offers shares of its stock to the public on a securities exchange. The screen is showing a table with several columns that include: - IPO Name: The name of the IPO. - Start Date: The date when the IPO starts. - End Date: The date when the IPO ends. - Price range: The range of the price per share for the IPO. - Minimum qty: The minimum quantity of shares an investor can bid for. Each IPO entry has buttons or links for actions like Apply and Details, allowing users to apply for the IPO or get more details about it. Some rows denote the 'Status' as 'Oversubscribed', while others show 'request pending' or have a 'Modify bid' option, which suggests that the platform allows for various stages of interaction with different IPOs. The top of the screen has menu options typical for an online service, including tabs like 'Dashboard', 'Portfolio', 'Reports', 'Support', and 'Account'. There's also a user icon indicating the possibility of accessing user profile settings or similar functionalities. This screenshot does not contain any sensitive information such as personal data, names, account numbers, or balances, and is a generic representation of a financial service platform."

    response = chat_with_openai(OPEN_AI_KEY, message, instructions)

    # Render the response in a simple HTML template
    return render_template('response.html', title='Chat API Response', response=response)


@bp.route('/scan-directory')
def scan_directory():
    return render_template('scan_directory.html')


@bp.route('/get-image-list')
def get_image_list():
    stored_descriptions = load_descriptions_map()  # Load stored descriptions
    image_paths = scan_directory_for_images(DIRECTORY_PATH)
    image_names = []
    processed_count = 0

    for path in image_paths:
        image_name = os.path.basename(path)
        if image_name not in stored_descriptions:
            image_names.append(image_name)
            processed_count += 1
            if processed_count >= IMAGE_LIMIT:
                break

    return jsonify({'images': image_names})


@bp.route('/process-image')
def process_image():
    image_name = request.args.get('image_path')
    image_path = os.path.join(DIRECTORY_PATH, image_name)
    existing_descriptions = load_descriptions_map()

    if image_name not in existing_descriptions:
        description = get_image_description(OPEN_AI_KEY, image_path)
        existing_descriptions[image_name] = description
        save_descriptions_map(existing_descriptions)
    else:
        description = existing_descriptions[image_name]

    return jsonify({'image_name': image_name, 'description': description})


@bp.route('/get-stored-data')
def get_stored_data():
    descriptions = load_descriptions_map()
    return render_template('get_stored_data.html', descriptions=descriptions)


@bp.route('/delete-stored-data')
def delete_stored_data():
    delete_descriptions_map()
    return jsonify({"message": "All stored data has been deleted."})
