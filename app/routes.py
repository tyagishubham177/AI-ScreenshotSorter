from flask import Blueprint, request, jsonify

bp = Blueprint('routes', __name__)


@bp.route('/')
def index():
    return "Welcome to ScreenshotSorter!"
