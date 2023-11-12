import os
import json


def scan_directory_for_images(directory_path):
    supported_extensions = ['.jpg', '.jpeg', '.png']
    image_paths = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if any(file.endswith(ext) for ext in supported_extensions):
                image_paths.append(os.path.join(root, file))
    return image_paths


def save_descriptions_map(descriptions_map, filename='image_descriptions.json'):
    with open(filename, 'w') as file:
        json.dump(descriptions_map, file)


def load_descriptions_map(filename='image_descriptions.json'):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def delete_descriptions_map(filename='image_descriptions.json'):
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass  # File does not exist, no action needed
    except Exception as e:
        print(f"Error deleting file: {e}")
