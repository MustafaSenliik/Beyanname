from flask import Blueprint, request, flash, render_template, redirect, url_for
from flask_login import login_required
from services.search_service import search_files, download_filtered_csv_service

# Blueprint tanımlaması
search_bp = Blueprint('search', __name__)

@search_bp.route('/search_page')
@login_required
def search_page():
    return render_template('index.html')

@search_bp.route('/search', methods=['GET'])
@login_required
def search():
    results = search_files(request.args)
    return render_template('index.html', results=results)

@search_bp.route('/download_filtered_csv')
@login_required
def download_filtered_csv():
    return download_filtered_csv_service(request.args)
