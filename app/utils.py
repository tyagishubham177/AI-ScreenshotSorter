import os
import json

from .openai_utils import chat_with_openai


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


def extract_labels(api_key, description):
    instructions = "From the user message, list in csv(no periods at end) important unique keyword tags that will categorize this image description. Use 3-5 tags for the description that highlight the image description."
    response = chat_with_openai(api_key, description, instructions)
    labels = response.rstrip('.').split(', ')
    return labels


def save_labels_map(labels_map, filename='labels_map.json'):
    with open(filename, 'w') as file:
        json.dump(labels_map, file)


def load_labels_map(filename='labels_map.json'):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def prune_similar_words(api_key, labels):
    try:
        labels_csv = ', '.join(labels)
        # Instructions to the API for pruning similar words
        instructions = "From user message, read CSV words, and remove redundant or similar words, that can be categorized as similar. Try to remove maximum redundancy. Remove as much similarity and duplication as you can."
        pruned_labels_csv = chat_with_openai(api_key, labels_csv, instructions)
        pruned_labels = pruned_labels_csv.rstrip('.').split(', ')
        return pruned_labels
    except Exception as e:
        print(f"Error in pruning labels: {e}")
        return labels  # Return original labels if error occurs
