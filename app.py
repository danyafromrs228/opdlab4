from flask import Flask, request, render_template
from collections import Counter
import re

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    text = file.read().decode('utf-8')
    words = re.findall(r'\b\w+\b', text.lower())
    word_counts = Counter(words)

    if word_counts:
        most_common = word_counts.most_common(1)[0]
        return f'Самое частое слово: "{most_common[0]}" (встречается {most_common[1]} раз)', 200
    return "Файл не содержит слов", 200