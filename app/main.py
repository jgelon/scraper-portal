from flask import Flask, render_template, request, redirect, url_for
from database import (
    init_db, add_entry, get_all_entries,
    get_entry_by_id, update_entry, delete_entry
)
from scraper import check_all_entries
from dotenv import load_dotenv
import threading
import time
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
init_db()

# Background thread for periodic scraping
def periodic_scrape():
    while True:
        print("Running periodic scrape...")
        check_all_entries()
        time.sleep(3600)  # Run every hour

@app.route('/')
def index():
    entries = get_all_entries()
    return render_template('index.html', entries=entries, edit_entry=None)

@app.route('/add', methods=['POST'])
def add():
    url = request.form['url']
    selector1 = request.form['selector1']
    selector2 = request.form.get('selector2') or None
    selector3 = request.form.get('selector3') or None
    add_entry(url, selector1, selector2, selector3)
    return redirect(url_for('index'))

@app.route('/edit/<int:entry_id>')
def edit(entry_id):
    entries = get_all_entries()
    entry = get_entry_by_id(entry_id)
    return render_template('index.html', entries=entries, edit_entry=entry)

@app.route('/update/<int:entry_id>', methods=['POST'])
def update(entry_id):
    url = request.form['url']
    selector1 = request.form['selector1']
    selector2 = request.form.get('selector2') or None
    selector3 = request.form.get('selector3') or None
    update_entry(entry_id, url, selector1, selector2, selector3)
    return redirect(url_for('index'))

@app.route('/delete/<int:entry_id>', methods=['POST'])
def delete(entry_id):
    delete_entry(entry_id)
    return redirect(url_for('index'))

@app.route('/scrape')
def scrapenow():
    print("Running scrape...")
    check_all_entries()
    return redirect(url_for('index'))

if __name__ == '__main__':
    thread = threading.Thread(target=periodic_scrape, daemon=True)
    thread.start()
    app.run(host='0.0.0.0', port=5000)
