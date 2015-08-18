from flask import Flask, request, render_template

app = Flask(__name__, static_url_path='')

'''
def search_for_autocomplete(partial_text):

'''

@app.route('/')
@app.route('/index')
def index():
    return render_template('app.html')

@app.route('/search', methods=['POST'])
def search():
    text = request.form['search']
    text = str(text)
    processed_text = text.upper()
    return processed_text

@app.route('/poop', methods=['GET'])
def poop():
    return render_template('poop.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
